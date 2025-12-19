import dayjs from 'dayjs';
import Dialog from '@vant/weapp/dialog/dialog';
import { request } from '../../utils/request'
// index.js
Page({
  data:{
    plan:[],
    record_id:''
  },
  editPlan(e){
    const index = e.currentTarget.dataset.index;
    const planItem = this.data.plan[index];
    const plan_id =planItem.plan_id
    wx.navigateTo({
      url: `/pages/edit/edit?plan_id=${plan_id}`
    });
  },

    onLoad(options){
      //向后端发送请求
      // const token = wx.getStorageSync('token')
      // console.log("token is "+ token)
     this.loadPlanList()
    },
    //检查此时state==true的个数
    countStateTrue(planList) {
      if (!Array.isArray(planList)) return 0;
    
      return planList.filter(item => item.state === true).length;
    },
    
loadPlanList(){
  // const token = wx.getStorageSync('token')
  // console.log(token)
  request({
    url: 'https://dailyshare.onrender.com/daily/fplan/',
    method:'GET',
    // header:{
    //   token :token
    // },
    success:(res)=>{
      if(res.data.code==100){
        this.setData({
          plan:res.data.result
        });
        // console.log(this.data.plan)
      }else{
        wx.showToast({
          title: 'network failure',
          
        })
      }
    }


  })
},
    planItemDelete(e){
      const index = e.currentTarget.dataset.index;
      const planItem = this.data.plan[index];
      const plan_id =planItem.plan_id
    
      wx.request({
        url: 'https://dailyshare.onrender.com/daily/plan/'+plan_id,
        method:"DELETE",
        success:()=>{
          this.loadPlanList()
        }
      })
    },
    changePlanState(e){
      const index = e.currentTarget.dataset.index;
      const planItem = this.data.plan[index];
      const isoString = dayjs().format('YYYY-MM-DDTHH:mm:ss');

      if(!planItem.state){
       if(!this.countStateTrue(this.data.plan)){ 
         wx.request({
          url:'https://dailyshare.onrender.com/daily/plan/'+planItem.plan_id,
          method:"PATCH",
          data:{"state":!planItem.state},
          success:()=>{
            this.loadPlanList();
            // this.setData({
            //   [`plan[${index}].state_text`]: this.data.plan[index].state_text + "从"+isoString+"开始"
            // });
            
          }

        });
        request({
          url: 'https://dailyshare.onrender.com/daily/record_add/',
          method:'POST',
          data:{
            "plan_name":planItem.plan_name,
            "start":isoString
          },
          success:(res)=>{
              this.setData({
                record_id:res.data.result.record_id
              })
              // console.log(this.data.record_id)
          }
        });


}else{
  // console.log("oops!")
  Dialog.alert({
    title: 'OOPS',
    message: '最多只能同时进行一项事务，请先完成正在进行的事务！',
  }).then(() => {
    // on close
  });
}
      
      }
      else{
        wx.request({
          url:'https://dailyshare.onrender.com/daily/plan/'+planItem.plan_id,
          method:"PATCH",
          data:{"state":!planItem.state},
          success:()=>{
            this.loadPlanList()
          }

        }),
        wx.request({
          url: 'https://dailyshare.onrender.com/daily/record/'+this.data.record_id,
          method:'PUT',
          data:{
            "upload":true,
            "end":isoString
          }
        })
      }

        
      
    },
    AddPlan(){
      wx.navigateTo(
        {url:"/pages/new/new"}
      )
    },
    onPullDownRefresh() {
      // 1. 重新请求数据
      this.loadPlanList()
      console.log("1")
  
      // 2. 请求完成后，手动停止刷新
      wx.stopPullDownRefresh();
      console.log("2")
    },
    onShow() {
      if (!wx.getStorageSync('token')) {
        wx.redirectTo({ url: '/pages/login/login' })
      }
      this.loadPlanList()
    },
    
    
    



})
