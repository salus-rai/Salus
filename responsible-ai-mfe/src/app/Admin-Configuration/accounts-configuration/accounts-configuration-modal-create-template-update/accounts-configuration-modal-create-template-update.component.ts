/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, Inject, Input, ViewChild } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { MatOption } from '@angular/material/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';
import { MatSelect } from '@angular/material/select';
import { MatSnackBar } from '@angular/material/snack-bar';
import { NonceService } from 'src/app/nonce.service';
import { UserValidationService } from 'src/app/services/user-validation.service';

@Component({
  selector: 'app-accounts-configuration-modal-create-template-update',
  templateUrl: './accounts-configuration-modal-create-template-update.component.html',
  styleUrls: ['./accounts-configuration-modal-create-template-update.component.css']
})
export class AccountsConfigurationModalCreateTemplateUpdateComponent {
  constructor(public dialogRef: MatDialogRef<AccountsConfigurationModalCreateTemplateUpdateComponent>, public _snackBar: MatSnackBar, private https: HttpClient, public dialog: MatDialog,public nonceService:NonceService,private validationService:UserValidationService,
     @Inject(MAT_DIALOG_DATA) public data: { id: any }) {
    this.fromCreation();
  }

  closeDialog() {
    this.dialogRef.close();
  }

  
  @ViewChild('select1') select1!: MatSelect;
  @ViewChild('select2') select2!: MatSelect;
  @ViewChild('select3') select3!: MatSelect;
  result: any;
  dataSource_getBatches: any;
  templateMappingGetUrl: any;


// SCREEN TWO ADD DATA  
//--------------VARIABLES-----------SECURITY

selectedReclist: any = [];
selectedReclist2: any = [];
allSelected1: any;
listShowlist1 = new Set();
allSelectedInput = false;
event1: any;
c1: boolean = false;
allSelected2: any;
listShowlist2 = new Set();
allSelectedInput2 = false;
event2: any;
c2: boolean = false;
userId =""
tab="Privacy"
dataSource: any = []
listReconList: any=[];
  customTemplateGetUrl: string="";
  responseArr:any=[]
  requestArr:any=[]
  tempalteArray:any=[]
  templateMappingPostUrl=""
  template_admin_update_addTempMap=""
  template_admin_get_selected_getTempMap=""
  selectedReclist3: any = [];
  allSelected3: any;
listShowlist3 = new Set();
allSelectedInput3 = false;
event3: any;
c3: boolean = false;
masterTemplateArr :any = ["Prompt Injection Check","Jailbreak Check","TOXICITY","PIIDETCT","REFUSAL","PROFANITY","RESTRICTTOPIC","Fairness and Bias Check"]
comparsionDropDownArr:any=[]
requestResonseDropDownArr:any=[]

  // select 1
toggleAllSelection1(event: any) {
  this.event1 = event;
  this.c1 = event.checked;
  this.allSelected1 = !this.allSelected1;
  if (this.allSelected1) {
    this.select1.options.forEach((item: MatOption) => {
      item.select();
      this.listShowlist1.add(item.value);
      const element = document.querySelector('[role="listbox"]');
      if (element instanceof HTMLElement) {
        element.style.display = 'none';
      }
      this.select1.close();
    });
  } else {
    this.select1.options.forEach((item: MatOption) => {
      item.deselect();

      this.listShowlist1.delete(item.value);
    });
  }
}
selectRecognizertype() {
  let newStatus = true;
  this.select1.options.forEach((item: MatOption) => {
    if (!item.selected) {
      newStatus = false;
      this.allSelected1 = false;
      this.listShowlist1.delete(item.value);
    } else {
      this.listShowlist1.add(item.value);
    }
  });
  this.allSelectedInput = newStatus;
}

  // select 2
  toggleAllSelection2(event: any) {
    this.event2 = event;
    this.c2 = event.checked;
    this.allSelected2 = !this.allSelected2;
    if (this.allSelected2) {
      this.select2.options.forEach((item: MatOption) => {
        item.select();
        this.listShowlist2.add(item.value);
        const element = document.querySelector('[role="listbox"]');
        if (element instanceof HTMLElement) {
          element.style.display = 'none';
        }
        this.select2.close();
      });
    } else {
      this.select2.options.forEach((item: MatOption) => {
        item.deselect();
  
        this.listShowlist2.delete(item.value);
      });
    }
  }
  selectRecognizertype2() {
    let newStatus = true;
    this.select2.options.forEach((item: MatOption) => {
      if (!item.selected) {
        newStatus = false;
        this.allSelected2 = false;
        this.listShowlist2.delete(item.value);
      } else {
        this.listShowlist2.add(item.value);
      }
    });
    this.allSelectedInput2 = newStatus;
  }


    // select 1
toggleAllSelection3(event: any) {
  this.event3 = event;
  this.c3 = event.checked;
  this.allSelected3 = !this.allSelected3;
  if (this.allSelected3) {
    this.select3.options.forEach((item: MatOption) => {
      item.select();
      this.listShowlist3.add(item.value);
      const element = document.querySelector('[role="listbox"]');
      if (element instanceof HTMLElement) {
        element.style.display = 'none';
      }
      this.select3.close();
    });
  } else {
    this.select3.options.forEach((item: MatOption) => {
      item.deselect();

      this.listShowlist3.delete(item.value);
    });
  }
}
selectRecognizertype3() {
  let newStatus = true;
  this.select3.options.forEach((item: MatOption) => {
    if (!item.selected) {
      newStatus = false;
      this.allSelected3 = false;
      this.listShowlist3.delete(item.value);
    } else {
      this.listShowlist3.add(item.value);
    }
  });
  this.allSelectedInput3 = newStatus;
}


  submit(){
    let payload ={
      "mapId":this.mapId,
      "userId": this.userId,
      "requestTemplate":this.templetUpdateFrom.get('requestTemplate')?.value,
      "responseTemplate":this.templetUpdateFrom.get('responseTemplate')?.value,
      "comparisonTemplate":this.templetUpdateFrom.get('comparisonTemplate')?.value
    }

    console.log("payload===",payload)
    this.patchtemplatet(payload)
  }
  patchtemplatet(payload: any){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    // this.https.patch("https://rai-toolkit-dev.az.ad.idemo-ppc.com/api/v1/rai/admin/addTempMap", payload, { headers }).subscribe((res:any)=>{
    this.https.patch(this.template_admin_update_addTempMap, payload, { headers }).subscribe
    ((res:any)=>{
      console.log("res===",res)
      // this.dialogRef.close();
      const message = "Template Updated Successfully"
      this.getslectedDropdownvalues()
      const action = "Close"
      this._snackBar.open(message, action, {
        duration: 3000,
        panelClass:['le-u-bg-black'],
      });
    },(error)=>{
            // You can access status:
            console.log(error)
            const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
            const action = "Close"
            this._snackBar.open(message, action, {
              duration: 3000,
              panelClass:['le-u-bg-black'],
            });})
  }
 

  getTemplateDetail(){
    
    
    // this.https.get(this.getUrl).subscribe
    // const getTemplateDetailLocalUrl="http://10.68.120.127:30016/api/v1/rai/admin/getCustomeTemplate/"
    this.https.get(this.customTemplateGetUrl+this.userId).subscribe
    ((res: any) => {
     
      this.result = res
      console.log("this.result===",this.result)
      this.dataSource_getBatches = res.templates;
      for(let i=0;i<this.dataSource_getBatches.length;i++){
        this.tempalteArray.push(this.dataSource_getBatches[i].templateName)
        
        // this.tempalteArray.push(this.)
      }
      this.comparsionDropDownArr = this.tempalteArray
      console.log("this.masterTemplateArr===",this.masterTemplateArr)
      this.tempalteArray = this.masterTemplateArr.concat(this.tempalteArray);
      console.log("this.tempalteArray===", this.tempalteArray);

      

      

    }  , error => {
      // You can access status:
      console.log(error)
      const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
      const action = "Close"
      this._snackBar.open(message, action, {
        duration: 3000,
        panelClass:['le-u-bg-black'],
      });

  })
    
}


  getLogedInUser() {
    let role = localStorage.getItem('role');
    console.log("role267===",role)  
    if (window && window.localStorage && typeof localStorage !== 'undefined') {
      const x = localStorage.getItem("userid") ? JSON.parse(localStorage.getItem("userid")!) : "NA";
      if (x != null && (this.validationService.isValidEmail(x) || this.validationService.isValidName(x))) {
        this.userId = x ;
      }
      console.log("userId", this.userId)
      
    }
  }

  getLocalStoreApi() {
    let ip_port
    if (localStorage.getItem("res") != null) {
      const x = localStorage.getItem("res")
      if (x != null) {
        return ip_port = JSON.parse(x)
      }
    }
  }

  setApilist(ip_port: any) {
      this.templateMappingPostUrl=ip_port.result.Admin + ip_port.result.ACCTEMPMAP 
    this.customTemplateGetUrl=ip_port.result.Admin + ip_port.result.TemplateGet
    this.templateMappingGetUrl=ip_port.result.Admin + ip_port.result.GETACCTEMPMAP 
    this.template_admin_update_addTempMap = ip_port.result.Admin + ip_port.result.Template_admin_update_addTempMap
    this.template_admin_get_selected_getTempMap = ip_port.result.Admin + ip_port.result.Template_admin_get_selected_getTempMap
    

    
  }

  reset(){

  }


  ngOnInit(): void {
    let ip_port: any
    this.getLogedInUser()

    ip_port = this.getLocalStoreApi()
    
    this.setApilist(ip_port)
    this.getTemplateDetail()
    this.getslectedDropdownvalues()
    
    
    
  }

  templetUpdateFrom!: FormGroup;
  fromCreation() {


    this.templetUpdateFrom = new FormGroup({
      requestTemplate: new FormControl([], [Validators.required]),
      responseTemplate: new FormControl([], [Validators.required]),
      comparisonTemplate: new FormControl([], [Validators.required]),
      
    });

  

  }
  mapId:any
  getslectedDropdownvalues(){
    const body = new URLSearchParams();
    body.set('accMasterId', this.data.id);
    

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });
    // this.https.post("https://rai-toolkit-dev.az.ad.idemo-ppc.com/api/v1/rai/admin/getTempMap", body.toString(), { headers }).subscribe
    this.https.post(this.template_admin_get_selected_getTempMap, body.toString(), { headers }).subscribe
    ((res:any)=>{
      // this.responseArr=res
      this.mapId=res[0].mapId
      // this.templetUpdateFrom.get('requestTemplate')?.setValue(res[0].requestTemplate)
      // this.templetUpdateFrom.get('responseTemplate')?.setValue(res[0].responseTemplate)
      // this.templetUpdateFrom.get('comparisonTemplate')?.setValue(res[0].comparisonTemplate)
      this.templetUpdateFrom.patchValue({
        requestTemplate: res[0].requestTemplate,
        responseTemplate: res[0].responseTemplate,
        comparisonTemplate: res[0].comparisonTemplate
      });

    },(error)=>{
            // You can access status:
            console.log(error)
            const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
            const action = "Close"
            this._snackBar.open(message, action, {
              duration: 3000,
              panelClass:['le-u-bg-black'],
            });})
      
  }

  
}
