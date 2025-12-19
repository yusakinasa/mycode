// utils/request.js

// const BASE_URL = 'http://127.0.0.1:8000';

function request(options) {
  const token = wx.getStorageSync('token');

  return new Promise((resolve, reject) => {
    wx.request({
      url: options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        token:token
      },
      success(res) {
        // 不做任何统一业务处理，原样返回
        options.success(res)
        resolve(res);
      },
      fail(err) {
        // 原样抛出错误
        options.fail(err)
        reject(err);
      }
    });
  });
}

module.exports = {
  request
};
