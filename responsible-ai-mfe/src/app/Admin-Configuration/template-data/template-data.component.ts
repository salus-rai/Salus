/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient } from '@angular/common/http';
import { Component, ElementRef, Inject, Input, ViewChild } from '@angular/core';
import { FormControl, FormGroup, UntypedFormBuilder, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
@Component({
  selector: 'app-template-data',
  templateUrl: './template-data.component.html',
  styleUrls: ['./template-data.component.css']
})
export class TemplateDataComponent {
  customTemplateUpdateUrl: any;
  selectedPrompt: string="";
  testPromptUrl: any;
  public safeTemplateData!: SafeHtml; 

  constructor(
    public dialogRef: MatDialogRef<TemplateDataComponent>,
    public https: HttpClient,
    private _snackBar: MatSnackBar,
    private fb: UntypedFormBuilder,
    private sanitizer: DomSanitizer,
    @Inject(MAT_DIALOG_DATA) public data: any
  ){}

  templateData:any
  update=false
  buttonName="Update"
  templateName:any
  userId:any
  mode:any
  template_type:any
  templateTest:any
  testAnalysis:any
  testResult:any
  promptTestOutput:any =false
  spinner = false
  promptValidation = false
  // userid: this.userId,
  // mode:this.CustomTemplateForm.value.mode ,
  // template_type:this.CustomTemplateForm.value.template_type

  // "subTemplates": [
  //               {
  //                   "_id": 1719386209.6371694,
  //                   "subTemplateId": 1719386209.6371694,
  //                   "templateId": 1719386209.61702,
  //                   "template": "evaluation_criteria",
  //                   "CreatedDateTime": "2024-06-26T12:46:49.637000",
  //                   "LastUpdatedDateTime": "2024-06-26T12:46:49.637000"
  //               },
  //               {
  //                   "_id": 1719386209.6437445,
  //                   "subTemplateId": 1719386209.6437445,
  //                   "templateId": 1719386209.61702,
  //                   "template": "prompting_instructions",
  //                   "CreatedDateTime": "2024-06-26T12:46:49.643000",
  //                   "LastUpdatedDateTime": "2024-06-26T12:46:49.643000"
  //               },
  //               {
  //                   "_id": 1719386209.6769922,
  //                   "subTemplateId": 1719386209.6769922,
  //                   "templateId": 1719386209.61702,
  //                   "template": "few_shot_examples",
  //                   "CreatedDateTime": "2024-06-26T12:46:49.676000",
  //                   "LastUpdatedDateTime": "2024-06-26T12:46:49.676000"
  //               }
  //           ]

  
  closeDialog(){
    this.dialogRef.close();
  }

  viewTemplateData(){
    this.buttonName="Submit"
    this.update=true
  }

  updateData(){
    const payload = {
      "userId": this.userId,
      "mode" : this.mode,
      "templateType": this.template_type,
      "templateName":this.templateName,
      "templateData":this.templateData
    }

    console.log("payload=================",payload)
    this.https.patch(this.customTemplateUpdateUrl,payload).subscribe((res)=>{
      console.log("res=================",res)
      
      this._snackBar.open("Template Saved Successfully", "Close", {
        duration: 2000,
      });
      this.closeDialog()
    })
  }
  updateTemplate(){
    // this.buttonName="Submit"
    // this.update=true

    if(this.update){
      this.updateData()

  }}

//   {
//     "uniqueid": "6a1202f703d64927a2fd9fbf23921f0d",
//     "userid": "admin",
//     "lotNumber": "1",
//     "created": "2024-06-27 11:21:19.263229",
//     "model": "gpt4",
//     "moderationResults": {
//         "response": [
//             {
//                 "question": "Hi",
//                 "score": 0,
//                 "threshold": 60,
//                 "analysis": "The user query 'Hi' is a simple greeting with no indication of prompt injection or any attempt to manipulate the system to reveal its underlying prompts or training instructions.",
//                 "result": "PASSED",
//                 "Tone Score": 3,
//                 "role": "Support",
//                 "Sentiment": "Neutral",
//                 "Domain": "General",
//                 "outputBeforemoderation": "Hello! How can I assist you today?",
//                 "outputAfterSentimentmoderation": "Hello! How can I assist you today?",
//                 "Context": "Initial Greeting",
//                 "timetaken": "5.524s"
//             }
//         ]
//     },
//     "evaluation_check": "Prompt Injection Check"
// }


  submit(){
    this.promptValidation=false
    if(this.selectedPrompt == ''){
      this.promptValidation = true
      return
    }
    console.log("selectedPrompt===",this.selectedPrompt)
    this.spinner=true
    const payload = {
      
        "AccountName": "None",
        "PortfolioName": "None",
        "userid": this.userId,
        "lotNumber": 1,
        "Prompt": this.selectedPrompt,
        "Context": "None",
        "Concise_Context": "None",
        "Reranked_Context": "None",
        "model_name": "gpt4",
        "temperature": "0",
        "PromptTemplate": "GoalPriority",
        "template_name": this.templateName
      
    }

    const localUrl = "http://10.68.120.127:30026/rai/v1/moderations/evalLLM"
    this.https.post(this.testPromptUrl,payload).subscribe((res:any)=>{

      this.testAnalysis = res["moderationResults"]["response"][0]["analysis"]
      this.testResult = res["moderationResults"]["response"][0]["result"]
      this.spinner=false
      this.promptTestOutput = true
      console.log("res=================",res)
    }, error => {
      // You can access status:
      console.log(error.status);


      // console.log(error.error.detail)
      console.log(error)
      const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
      const action = "Close"
      this._snackBar.open(message, action, {
        duration: 3000,
        horizontalPosition: 'left',
        panelClass: ['le-u-bg-black'],
      });


    }
    )

    console.log("payload======",payload)
  }

  resetForm(){
    this.selectedPrompt = '';
  }

  // getLogedInUser() {
  //   if (localStorage.getItem("userid") != null) {
  //     const x = localStorage.getItem("userid")
  //     if (x != null) {

  //       this.userId = JSON.parse(x)
  //       console.log(" userId", this.userId)
  //       return JSON.parse(x)
  //     }

  //     console.log("userId", this.userId)
  //   }
  // }

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
    
    this.customTemplateUpdateUrl=ip_port.result.Admin + ip_port.result.TemplateUpdate 
    this.testPromptUrl = ip_port.result.Admin + ip_port.result.TestTemplate

   
  }

  ngOnInit(): void {
    let ip_port: any

    // let user = this.getLogedInUser()

    ip_port = this.getLocalStoreApi()
    this.setApilist(ip_port)

    this.templateData=this.data.dataValue
    this.templateName = this.data.templateName
    this.mode = this.data.mode
    this.userId = this.data.userid
    this.template_type = this.data.template_type
    this.templateTest = this.data.templateTest
    console.log("data================",this.data)
  }
   // Function to sanitize the data before it is used
   sanitizeData(data: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(data);
  }
}
