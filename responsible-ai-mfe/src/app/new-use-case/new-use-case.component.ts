/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient } from '@angular/common/http';
import { ChangeDetectorRef, Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { HomeService } from '../home/home.service';
import { UseCaseServiceService } from '../use-case-parent/use-case-service.service';


@Component({
  selector: 'app-new-use-case',
  templateUrl: './new-use-case.component.html',
  styleUrls: ['./new-use-case.component.css']
})
export class NewUseCaseComponent {
  isLoadingUseCase = true;
  userId=""
  createUseCase: any;
  getUseCase: any;
  dataSource = []
  result: any;
  useCaseNameDetail = []
  useCaseName:any
  useCaseScreen=true
  record=false
  newUseCaseCreation=false
  getAICanvasEndPoint: any;
  dataRecieved=false
  edit=false
  getRaiICanvasEndPoint: any;
  activeTab = "Available Use cases";
  constructor(private _snackBar: MatSnackBar,private useCaseService:UseCaseServiceService,private _formBuilder: FormBuilder,private cdr: ChangeDetectorRef,public https: HttpClient,private modalservice: NgbModal,private router:Router) {
    this.edit=false
    console.log("From constructor edit value====",this.edit)
  }



  getLogedInUser() {
    if (localStorage.getItem("userid") != null) {
      const x = localStorage.getItem("userid")
      if (x != null) {

        this.userId = JSON.parse(x)
        console.log(" userId", this.userId)
        return JSON.parse(x)
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
  getUseCaseDetail(userId:any){
    console.log("Userid============",userId)
    // this.https.get(this.getUrl+userId).subscribe
    this.https.get(this.getUseCase+'"'+userId+'"').subscribe
    ((res: any) => {

      this.result = res
      console.log("Result====",res)
      console.log("lenght -f res=====",res.length)
      console.log("Result====",res[0].useCaseName)
      this.useCaseNameDetail=res[0].useCaseName
      console.log("useCaseNameDetail====",this.useCaseNameDetail)
      this.dataSource = res[0].useCaseName

      // const element = {
      //   "viewValue": this.dataSource[i],
      //   "value": this.dataSource[i]
      // }
      // console.log("This element===",element)
      // this.dropDown.push(element)

      // for(let i=0;i<this.dataSource.length;i++){
      //   console.log("This Datasorce===",this.dataSource[i])
      //   const element = {
      //     "viewValue": this.dataSource[i],
      //     "value": this.dataSource[i]
      //   }
      //   console.log("This element===",element)
      //   this.dropDown.push(element)
      // }
      // console.log("This Datasorce187===",this.dropDown)
      // this.dataSource1  = res[0].useCaseName
      // console.log("This Datasorce1189===",this.dataSource)

      this.cdr.detectChanges();

      this.isLoadingUseCase = false;



    }  , error => {


      // this.showSpinner1 = false;

      // console.log(error.error.detail)
      console.log(error)
      const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
      const action = "Close"
      this._snackBar.open(message, action, {
        duration: 3000,
        panelClass:['le-u-bg-black'],
      });

  })
    this.cdr.detectChanges();
  }

setApilist(ip_port: any) {
      // this.getFile = ip_port.result.DocProcess + ip_port.result.DocProcess_getFiles  // + environment.getFile
      // this.uploadFile = ip_port.result.DocProcess + ip_port.result.DocProcess_uploadFile   //+ environment.uploadFile
      // this.DocProcessing_getFileContent = ip_port.result.DocProcess + ip_port.result.DocProcessing_getFileContent   //+ environment.uploadFile
      this.createUseCase =ip_port.result.Questionnaire + ip_port.result.Questionnaire_createUsecase
      this.getUseCase = ip_port.result.Questionnaire + ip_port.result.Questionnaire_getUsecaseDetail
      this.getAICanvasEndPoint = ip_port.result.Questionnaire + ip_port.result.AI_Canvas_Response
      this.getRaiICanvasEndPoint = ip_port.result.Questionnaire + ip_port.result.Canvas_Response

      // this.getUseCaseDetail(this.userId)
    }




    editForm (usecaseName:any){

      this.useCaseService.setEditParameter(true)
      this.useCaseService.setUseCaseName(usecaseName)
        // let getURL = this.apiURL + this.getAICanvasEndPoint 
        // console.log("getURL::",getURL)
        // this.https.get(this.localgetUrl+ userId +"/"+ AiUseCaseName).subscribe(
        this.https.get(this.getAICanvasEndPoint+ '"'+this.userId+'"' +"/"+ usecaseName).subscribe(
          (res: any) => {
            if (res == "No Record Found") {
              console.log("No Record Found")
              // this.aiCanvasEdit = true;
              this.cdr.detectChanges();
              return
            }else{
              console.log("Ai Canvas Data==========",res);
              this.useCaseService.setAiCanvas(res)
              this.edit=true
              this.dataRecieved =true
              if(res.BusinessProblem == "" && res.BusinessValue == "" && res.EndUserValue == "" && res.DataStrategy == "" && res.ModellingApproach == "" && res.ModelTraining == "" && res.ObjectiveFunction == "" && res.AICloudEngineeringServices == "" && res.ResponsibleAIApproach == ""){
                console.log("All values are empty")
                // this.aiCanvasEdit = true;
                this.cdr.detectChanges();
                return
              }
             
              // this.aiCanvasEdit = false;
              this.cdr.detectChanges();
            }
          },
          error => {
            console.log(error);
          }
        );


        this.https.get(this.getRaiICanvasEndPoint+ '"'+this.userId+'"' +"/"+ usecaseName).subscribe(
          (res: any) => {
            if (res == "No Record Found") {
              console.log("No Record Found")
              // this.aiCanvasEdit = true;
              this.cdr.detectChanges();
              return
            }else{
              console.log("RAi Canvas Data from new use case==========",res);
              this.useCaseService.setRaiCanvas(res)
              this.edit=true
              if(res.Accountability == "" && res.SecurityVulnerabilities == "" && res.Explainability == "" && res.StandardMLopsPractices == "" && res.Fairness == "" && res.Drift == "" && res.HumanTouchPoints == "" && res.RobustnessAndRisks == "" && res.Privacy == ""){
                console.log("All values are empty")
                // this.raiCanvasEdit = true;
                this.cdr.detectChanges();
                return
              }
             
              // this.aiCanvasEdit = false;
              this.cdr.detectChanges();
            }
          },
          error => {
            console.log(error);
          }
        );
      

    }
  ngOnInit(){

    let ip_port: any

  let user = this.getLogedInUser()

  ip_port = this.getLocalStoreApi()
  this.setApilist(ip_port)
  this.useCaseService.setUseCaseName("")
          this.useCaseService.setAiCanvas("")
          this.useCaseService.setRaiCanvas("")
          this.useCaseService.setEditParameter(false)
          this.useCaseService.setMessage(1)
  this.getUseCaseDetail(this.userId)
  // this.getDetails()
  }


  generateReport(useCaseName:any){
    this.useCaseName=useCaseName
    this.record=true
    this.useCaseService.setGenerateReport(false)
    // this.router.navigate(['/use-case-report'])
    console.log("Generate Report",useCaseName)
  }

  openRightSideModal(){
    this.newUseCaseCreation=true
    this.useCaseScreen=false
  }
  selectedTabValue(event: any) {
    this.activeTab = event.tab.textLabel;
    console.log('tab', this.activeTab);
  }}
