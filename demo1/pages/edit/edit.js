// pages/new/new.js
Page({
  data:{
    /**
     * 页面的初始数据
     */
    form: {
      plan_name:'',
      start_time:'',
      end_time:'',
    },
    
      minHour: 10,
      maxHour: 23,
      plan_id:0
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
        start_time: this.data.form.start_time + ':00',
        end_time: this.data.form.end_time + ':00',
        "is_fixed":true,
        "user_id":1
      };
  
      // console.log('最终提交的 JSON：', payload);
      wx.request({
        url: 'http://127.0.0.1:8000/daily/plan/'+this.data.plan_id,
        method:"PUT",
        data:payload,
        success:()=>{
          // console.log("success!")
          wx.navigateBack()
        }
      })
    },
    onTimeConfirm(e) {
      const field = e.currentTarget.dataset.field;
      const value = e.detail; // "HH:mm"
    
      this.setData({
        [`form.${field}`]: value
      });
    },
    

    loadPlanDetail(plan_id) {
      wx.request({
        url: `http://127.0.0.1:8000/daily/plan/${plan_id}`,
        method: 'GET',
        success: (res) => {
          if (res.data.code === 100) {
            const plan = res.data.result;
            this.setData({
              form: {
                plan_name: plan.plan_name,
                start_time: plan.start_time.slice(0, 5),
                end_time: plan.end_time.slice(0, 5)
              }
            });
          }
        }
      });
    },
    
  
    /**
     * 生命周期函数--监听页面加载
     */
    onLoad(options) {
        this.setData({
          plan_id: options.plan_id
        });
        this.loadPlanDetail(options.plan_id);
      
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