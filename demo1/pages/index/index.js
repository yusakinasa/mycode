
// index.js
Page({
  data:{
    plan:[]
  },

    onLoad(options){
      //向后端发送请求
     this.loadPlanList()
    },
loadPlanList(){
  wx.request({
    url: 'http://127.0.0.1:8000/daily/fplan/',
    method:'GET',
    success:(res)=>{
      if(res.data.code==100){
        this.setData({
          plan:res.data.result
        })
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
    }



})
