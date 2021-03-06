import numpy as np
# from im2col import im2col_indices

def affine_forward(x, w, b):
  """
  Computes the forward pass for an affine (fully-connected) layer.

  The input x has shape (N, d_1, ..., d_k) where x[i] is the ith input.
  We multiply this against a weight matrix of shape (D, M) where
  D = \prod_i d_i

  Inputs:
  x - Input data, of shape (N, d_1, ..., d_k)
  w - Weights, of shape (D, M)
  b - Biases, of shape (M,)
  
  Returns a tuple of:
  - out: output, of shape (N, M)
  - cache: (x, w, b)
  """
  out = None
  #############################################################################
  # TODO: Implement the affine forward pass. Store the result in out. You     #
  # will need to reshape the input into rows.                                 #
  #############################################################################
  x_row_shape = x.reshape(x.shape[0], np.prod(x.shape[1:]))
  out = np.dot(x_row_shape, w) + b
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b)
  return out, cache


def affine_backward(dout, cache):
  """
  Computes the backward pass for an affine layer.

  Inputs:
  - dout: Upstream derivative, of shape (N, M)
  - cache: Tuple of:
    - x: Input data, of shape (N, d_1, ... d_k)
    - w: Weights, of shape (D, M)

  Returns a tuple of:
  - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
  - dw: Gradient with respect to w, of shape (D, M)
  - db: Gradient with respect to b, of shape (M,)
  """
  x, w, b = cache
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the affine backward pass.                                 #
  #############################################################################
  x_row_shape = x.reshape(x.shape[0], np.prod(x.shape[1:]))
  dw = np.dot(x_row_shape.T, dout)
  db = np.sum(dout, axis=0)
  dx = np.reshape(np.dot(dout, w.T), x.shape)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def relu_forward(x):
  """
  Computes the forward pass for a layer of rectified linear units (ReLUs).

  Input:
  - x: Inputs, of any shape

  Returns a tuple of:
  - out: Output, of the same shape as x
  - cache: x
  """
  out = None
  #############################################################################
  # TODO: Implement the ReLU forward pass.                                    #
  #############################################################################
  out = x * (x > 0)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = x
  return out, cache


def relu_backward(dout, cache):
  """
  Computes the backward pass for a layer of rectified linear units (ReLUs).

  Input:
  - dout: Upstream derivatives, of any shape
  - cache: Input x, of same shape as dout

  Returns:
  - dx: Gradient with respect to x
  """
  dx, x = None, cache
  #############################################################################
  # TODO: Implement the ReLU backward pass.                                   #
  #############################################################################
  dx = dout.copy()
  dx[x <= 0] = 0
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def conv_forward_naive(x, w, b, conv_param):
  """
  A naive implementation of the forward pass for a convolutional layer.

  The input consists of N data points, each with C channels, height H and width
  W. We convolve each input with F different filters, where each filter spans
  all C channels and has height HH and width HH.

  Input:
  - x: Input data of shape (N, C, H, W)
  - w: Filter weights of shape (F, C, HH, WW)
  - b: Biases, of shape (F,)
  - conv_param: A dictionary with the following keys:
    - 'stride': The number of pixels between adjacent receptive fields in the
      horizontal and vertical directions.
    - 'pad': The number of pixels that will be used to zero-pad the input.

  Returns a tuple of:
  - out: Output data, of shape (N, F, H', W') where H' and W' are given by
    H' = 1 + (H + 2 * pad - HH) / stride
    W' = 1 + (W + 2 * pad - WW) / stride
  - cache: (x, w, b, conv_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the convolutional forward pass.                           #
  # Hint: you can use the function np.pad for padding.                        #
  #############################################################################
  (N, C, H, W) = x.shape
  (F, _, HH, WW) = w.shape
  stride, pad = conv_param['stride'], conv_param['pad']
  H_out = 1 + (H + 2 * pad - HH) / stride
  W_out = 1 + (W + 2 * pad - WW) / stride
  if type(H_out) != int or type(W_out) != int:
    raise Exception('Invalid output dimension')
  H_out, W_out = int(H_out), int(W_out)
  out = np.zeros((N, F, H_out, W_out))

  # x_cols = im2col_indices(x, HH, WW, padding=pad, stride=stride)
  # w_cols = w.reshape(N, -1)
  # # print w_cols.shape
  # out = (w_cols @ x_cols) + b
  # out = out.reshape(F, H_out, W_out, N)
  # out = out.transpose(3, 0, 1, 2)
  for n in xrange(N):
    x_padded = np.pad(x[n, :, :, :], ((0, 0),(pad, pad),(pad, pad)), 'constant')
    for f in xrange(F):
      for ho in xrange(H_out):
        for wo in xrange(W_out):
          h1 = ho * stride
          h2 = h1 + HH
          w1 = wo * stride
          w2 = w1 + WW
          window = x_padded[:, h1:h2, w1:w2]
          out[n, f, ho, wo] = np.sum(window * w[f,:,:,:]) + b[f]
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b, conv_param)
  return out, cache


def conv_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a convolutional layer.

  Inputs:
  - dout: Upstream derivatives.
  - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

  Returns a tuple of:
  - dx: Gradient with respect to x
  - dw: Gradient with respect to w
  - db: Gradient with respect to b
  """
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the convolutional backward pass.                          #
  #############################################################################
  (x, w, b, conv_param) = cache
  (N, C, H, W) = x.shape
  (F, _, HH, WW) = w.shape
  stride, pad = conv_param['stride'], conv_param['pad']
  H_out = 1 + (H + 2 * pad - HH) / stride
  W_out = 1 + (W + 2 * pad - WW) / stride
  if type(H_out) != int or type(W_out) != int:
    raise Exception('Invalid output dimension')
  H_out, W_out = int(H_out), int(W_out)
  
  dx = np.zeros_like(x)
  dw = np.zeros_like(w)
  db = np.zeros_like(b)
  for n in xrange(N):
    x_padded = np.pad(x[n, :, :, :], ((0, 0),(pad, pad),(pad, pad)), 'constant')
    dx_padded = np.pad(dx[n, :, :, :], ((0, 0),(pad, pad),(pad, pad)), 'constant')
    for f in xrange(F):
      for ho in xrange(H_out):
        for wo in xrange(W_out):
          h1 = ho * stride
          h2 = h1 + HH
          w1 = wo * stride
          w2 = w1 + WW
          dx_padded[:, h1:h2, w1:w2] += w[f, :, :, :] * dout[n, f, ho, wo]
          dw[f, :, :, :] += x_padded[:, h1:h2, w1:w2] * dout[n, f, ho, wo]
          db[f] += dout[n, f, ho, wo]
    dx[n, :, :, :] = dx_padded[:, pad:-pad, pad:-pad]

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def max_pool_forward_naive(x, pool_param):
  """
  A naive implementation of the forward pass for a max pooling layer.

  Inputs:
  - x: Input data, of shape (N, C, H, W)
  - pool_param: dictionary with the following keys:
    - 'pool_height': The height of each pooling region
    - 'pool_width': The width of each pooling region
    - 'stride': The distance between adjacent pooling regions

  Returns a tuple of:
  - out: Output data
  - cache: (x, pool_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the max pooling forward pass                              #
  #############################################################################
  (N, C, H, W) = x.shape
  ph, pw, stride = pool_param['pool_height'], pool_param['pool_width'], pool_param['stride']
  H_out = 1 + (H - ph) / stride
  W_out = 1 + (W - pw) / stride
  out = np.zeros((N, C, H_out, W_out))

  for n in xrange(N):
    for h in xrange(H_out):
      for w in xrange(W_out):
        h1 = h * stride
        h2 = h1 + ph
        w1 = w * stride
        w2 = w1 + pw
        window = x[n, :, h1:h2, w1:w2]
        out[n, :, h, w] = np.max(window.reshape((C, ph * pw)), axis=1)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, pool_param)
  return out, cache


def max_pool_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a max pooling layer.

  Inputs:
  - dout: Upstream derivatives
  - cache: A tuple of (x, pool_param) as in the forward pass.

  Returns:
  - dx: Gradient with respect to x
  """
  dx = None
  #############################################################################
  # TODO: Implement the max pooling backward pass                             #
  #############################################################################
  (x, pool_param) = cache
  (N, C, H, W) = x.shape
  ph, pw, stride = pool_param['pool_height'], pool_param['pool_width'], pool_param['stride']
  H_out = 1 + (H - ph) / stride
  W_out = 1 + (W - pw) / stride
  dx = np.zeros_like(x)

  for ii, i in enumerate(xrange(0, H, stride)):
    for jj, j in enumerate(xrange(0, W, stride)):
      max_index = np.argmax(x[:, :, i:i+ph, j:j+pw].reshape(N, C, -1), axis=2)
      max_cols = np.remainder(max_index, pw) + j
      max_rows = max_index / pw + i
      for n in xrange(N):
        for c in xrange(C):
          dx[n, c, max_rows[n, c], max_cols[n, c]] += dout[n, c, ii, jj]

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def svm_loss(x, y):
  """
  Computes the loss and gradient using for multiclass SVM classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  N = x.shape[0]
  correct_class_scores = x[np.arange(N), y]
  margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
  margins[np.arange(N), y] = 0
  loss = np.sum(margins) / N
  num_pos = np.sum(margins > 0, axis=1)
  dx = np.zeros_like(x)
  dx[margins > 0] = 1
  dx[np.arange(N), y] -= num_pos
  dx /= N
  return loss, dx


def softmax_loss(x, y):
  """
  Computes the loss and gradient for softmax classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  probs = np.exp(x - np.max(x, axis=1, keepdims=True))
  probs /= np.sum(probs, axis=1, keepdims=True)
  N = x.shape[0]
  loss = -np.sum(np.log(probs[np.arange(N), y])) / N
  dx = probs.copy()
  dx[np.arange(N), y] -= 1
  dx /= N
  return loss, dx

