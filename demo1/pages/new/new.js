// pages/new/new.js
import { request } from '../../utils/request'

Page({
data:{
  /**
   * 页面的初始数据
   */
  form: {
    plan_name:'',
    start_time:'12:00',
    end_time:'12:00',
  },
  
    minHour: 10,
    maxHour: 20,
  },

  onFieldChange(e) {
    const field = e.currentTarget.dataset.field;
    const value = e.detail;

    this.setData({
      [`form.${field}`]: value
    });
  },

  updatePlan(){
    const payload = {
      ...this.data.form,
      "is_fixed":true,
      
    };

    console.log('最终提交的 JSON：', payload);
    request({
      url: 'https://dailyshare.onrender.com/daily/fplan/',
      method:"POST",
      data:payload,
      success:()=>{
        console.log("success!")
        wx.navigateBack()
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