import dayjs from 'dayjs';
import Dialog from '@vant/weapp/dialog/dialog';
// index.js
Page({
  data:{
    plan:[],
    record_id:''
  },
  editPlan(e){
    const plan_id =e.currentTarget.dataset.index+1; 
    wx.navigateTo({
      url: `/pages/edit/edit?plan_id=${plan_id}`
    });
  },

    onLoad(options){
      //向后端发送请求
     this.loadPlanList()
    },
    //检查此时state==true的个数
    countStateTrue(planList) {
      if (!Array.isArray(planList)) return 0;
    
      return planList.filter(item => item.state === true).length;
    },
    
loadPlanList(){
  wx.request({
    url: 'http://127.0.0.1:8000/daily/fplan/',
    method:'GET',
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
      const plan_id =e.currentTarget.dataset.index+1; 
      // console.log('http://127.0.0.1:8000/daily/plan/'+plan_id,)
      wx.request({
        url: 'http://127.0.0.1:8000/daily/plan/'+plan_id,
        method:"DELETE",
        success:()=>{
          this.loadPlanList()
        }
      })
    },
    changePlanState(e){
      const index = e.currentTarget.dataset.index;
      const planItem = this.data.plan[index];
      // const now = new Date();
      // // console.log(now)
      // const isoString = now.toISOString().split('.')[0]; // 去掉毫秒
      const isoString = dayjs().format('YYYY-MM-DDTHH:mm:ss');
      // console.log(isoString); 
// 示例输出: "2025-12-17T17:04:00"

      if(!planItem.state){
       if(!this.countStateTrue(this.data.plan)){ wx.request({
          url:'http://127.0.0.1:8000/daily/plan/'+(index+1),
          method:"PATCH",
          data:{"state":!planItem.state},
          success:()=>{
            this.loadPlanList()
          }

        });
        wx.request({
          url: 'http://127.0.0.1:8000/daily/records/',
          method:'POST',
          data:{
            "plan_name":planItem.plan_name,
            "user_id":1,
            "start":isoString
          },
          success:(res)=>{
              this.setData({
                record_id:res.data.result.record_id
              })
              // console.log(this.data.record_id)
          }
        })
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
          url:'http://127.0.0.1:8000/daily/plan/'+(index+1),
          method:"PATCH",
          data:{"state":!planItem.state},
          success:()=>{
            this.loadPlanList()
          }

        }),
        wx.request({
          url: 'http://127.0.0.1:8000/daily/record/'+this.data.record_id,
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
  
      // 2. 请求完成后，手动停止刷新
      wx.stopPullDownRefresh();
    },



})
