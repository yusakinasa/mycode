// pages/my/my.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
      record:[
      ]
  },
  loadRecordList(){
    wx.request({
      url: 'http://127.0.0.1:8000/daily/records/',
      method:'GET',
      success:(res)=>{
        if(res.data.code==100){
          this.setData({
            record:res.data.result
          })
        }else{
          wx.showToast({
            title: 'network failure',
            
          })
        }
      }
  
  
    })
  },

  onPullDownRefresh() {
    // 1. 重新请求数据
    this.loadRecordList()

    // 2. 请求完成后，手动停止刷新
    wx.stopPullDownRefresh();
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.loadRecordList()
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})