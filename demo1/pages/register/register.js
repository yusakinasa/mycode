// pages/register/register.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    form:{
      "username":'',
      "password":''
    }
  },
  onFieldChange(e) {
    const field = e.currentTarget.dataset.field;
    const value = e.detail;

    this.setData({
      [`form.${field}`]: value
    });
  },
  updateUser(){
    const payload = {
      ...this.data.form
    };

    console.log('最终提交的 JSON：', payload);
    wx.request({
      url: 'https://dailyshare.onrender.com/daily/auth/user/create/',
      method:"POST",
      data:payload,
      success:(res)=>{
        if(res.data.code==100)
        {console.log("success!")
        wx.navigateBack()}
        if(res.data.code==400){
          console.log("该用户名已经存在！")
        }
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

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