/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient } from '@angular/common/http';
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { PagingConfig } from '../_models/paging-config.model';
import { environment } from 'src/environments/environment';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { RoleManagerService } from '../services/role-maganer.service';


@Component({
  selector: 'app-unstructured-text',
  templateUrl: './unstructured-text.component.html',
  styleUrls: ['./unstructured-text.component.css']
})
export class UnstructuredTextComponent implements OnInit, PagingConfig {
  currentPage: number = 1;
  itemsPerPage: number = 5;
  totalItems: number = 0;
  // FOR SHIMMER EFFECT
  isLoadingUpload = true;
  isLoadingSelectType=true;
  isLoadingTable = true;
  ///////////
  pagingConfig: PagingConfig = {} as PagingConfig;

  uploadMode = false;
  promptMode = true;

  tableSize: number[] = [5, 10, 15, 20];

  form: FormGroup;

  dataSource: any = [];

  p: number = 1;

  constructor(private https: HttpClient, private fb: FormBuilder, private snackBar: MatSnackBar, public roleService: RoleManagerService) {
    this.pagingConfig = {
      itemsPerPage: this.itemsPerPage,
      currentPage: this.currentPage,
      totalItems: this.totalItems
    }
    this.form = this.fb.group({
      file: [null, Validators.required],
      options: [null, Validators.required]
    });
  }

  files: any[] = [];
  demoFile: any[] = [];
  selectedFile: File | any;
  file: File | any;
  user = "admin"
  showSpinner1 = false;
  tenantarr: any = []
  selectedOptions: any = []
  options: any = ["Privacy", "Profanity", "FM-Moderation", "Explainability"]



  // lotNumber: any;
  imageEnv = environment.imagePathurl + '/assets/image/';
  imgType = ".png"
  PrivacyIcon = environment.imagePathurl + '/assets/image/Privacy.png'
  fmIcon = environment.imagePathurl + '/assets/image/fm.png'
  explainabilityIcon = environment.imagePathurl + '/assets/image/explainability.png'
  ProfanityIcon = environment.imagePathurl + '/assets/image/Safety.png'
  Icon = "Icon"


  fm_api: any;
  fm_config_getAttributes: any;
  Moderationlayer_openaiCOT: any;
  fm_api_openAi: any;
  lot_assign: any;
  lot_details: any;
  priAnalyze: any
  priAnonymize: any;
  profAnalyze: any;
  profCensor: any;
  explainability: any;
  moderationCOV: any;
  coupledModerations: any;
  ModerationOpenai: any;
  fm_admin_UserRole: any;
  nemo_ModerationRail: any;
  Workbench_UploadFile: any

  favoriteSeason: any // Initialize the favoriteSeason property
  Select_types: string[] = ['Privacy', 'Profanity', 'FM Moderation', 'Exaplainability'];
  onFileChange(event: any) {
    const reader = new FileReader();
    reader.onload = (e: any) => {
      const text = e.target.result;
      console.log(text);
    };
    reader.readAsText(event.target.files[0]);
  }

  ngOnInit(): void {
    this.options = this.roleService.getSelectedTypeOptions("Workbench", "Unstructured-Text", "Traditional-AI")
    if (!this.roleService.checkActiveTabExists('Workbench', 'Unstructured-Text', 'Traditional-AI')) {
      this.uploadMode = false;
      this.promptMode = true;
    }
    console.log("This is unstructured text component")
    let ip_port: any
    // user call should happen here
    this.user = this.getLogedInUser()
    // geting list of api from  local sotragge
    ip_port = this.getLocalStoreApi()

    // seting up api list
    this.setApilist(ip_port)
    this.getLotDetails(this.user)

  }
  getLogedInUser() {
    if (localStorage.getItem("userid") != null) {
      const x = localStorage.getItem("userid")
      if (x != null) {
        // this.userId = JSON.parse(x)
        return JSON.parse(x)
      }
    }
  }

  ontoglechange(event: any) {
    if (event.checked == true) {
      this.uploadMode = false;
      this.promptMode = true;
    } else {
      this.uploadMode = true;
      this.promptMode = false;
    }
  }

  // used to set the api list urls
  setApilist(ip_port: any) {
    this.priAnalyze = ip_port.result.Privacy + ip_port.result.Privacy_text_analyze
    this.priAnonymize = ip_port.result.Privacy + ip_port.result.Privacy_text_anonymize
    this.profAnalyze = ip_port.result.Profanity + ip_port.result.Profanity_text_analyze;
    this.profCensor = ip_port.result.Profanity + ip_port.result.Profanity_text_censor;
    this.explainability = ip_port.result.Explainability;
    this.moderationCOV = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_COV;
    this.coupledModerations = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_completions;
    this.ModerationOpenai = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_openai;
    this.fm_admin_UserRole = ip_port.result.Admin + ip_port.result.Admin_userRole;
    this.nemo_ModerationRail = ip_port.result.Nemo + ip_port.result.Nemo_ModerationRail


    // fm
    this.fm_api = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_completions // + environment.fm_api
    this.fm_config_getAttributes = ip_port.result.Admin + ip_port.result.Fm_Config_GetAttributes;
    this.Moderationlayer_openaiCOT = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_openaiCOT
    this.fm_api_openAi = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_openai     //+ environment.fm_api_openAi
    // for lot assign
    this.lot_assign = ip_port.result.Questionnaire + ip_port.result.AssignLot;
    this.lot_details = ip_port.result.Questionnaire + ip_port.result.AllLotDetails;
    this.Workbench_UploadFile = ip_port.result.Questionnaire + ip_port.result.Workbench_UploadFile;
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
  getLotDetails(user: any) {
    this.dataSource = [];
    const getUrl = this.lot_details + user;
    // this.dataSource = this.test
    console.log("This .getUrl====", getUrl)
    this.https.get(getUrl).subscribe(
      (res: any) => {
        if (!Array.isArray(res)) {
          console.log("No Records Found");
          // this.cdr.detectChanges();
          this.isLoadingUpload = false;
          this.isLoadingSelectType = false;
          this.isLoadingTable = false;
          return
        }
        else {
          console.log("Records Found")
          console.log("Res:", res)
          this.dataSource = res;
          this.pagingConfig.totalItems = this.dataSource.length;


          // console.log("This .datasource====",this.dataSource)
        }
        // give isloadingupload delay of 5 sec

        this.isLoadingUpload = false;


        this.isLoadingSelectType = false;
        this.isLoadingTable = false;



        // this.isLoadingUpload=false;
      })
  }
  onTableDataChange(event: any) {
    this.currentPage = event;
    this.pagingConfig.currentPage = event;
    this.pagingConfig.totalItems = this.dataSource.length;
  }
  onTableSizeChange(event: any): void {
    this.pagingConfig.itemsPerPage = event.target.value;
    this.pagingConfig.currentPage = 1;
    this.pagingConfig.totalItems = this.dataSource.length;
  }

  fileBrowseHandler(imgFile: any) {
    const allowedTypes = ['text/csv'];
    console.log("fileBrowseHandler", imgFile.target.files[0].type)
    if (!allowedTypes.includes(imgFile.target.files[0].type)) {
      this.snackBar.open('Please select a valid file type', '✖', {
        horizontalPosition: 'center',
        verticalPosition: 'top',
        duration: 3000,
      });
      // return;
    }else{
    // this.browseFilesLenth = imgFile.target.files.length;
    this.prepareFilesList(imgFile.target.files);
    this.demoFile = this.files;
    this.file = this.files[0];
    // this.uploadDocument(this.file);
    //  console.log("on choosing")
    this.form.patchValue({
      file: this.files[0]
    });
  }
  }

  prepareFilesList(files: Array<any>) {
    this.files = []
    for (const item of files) {
      const cleanedName = item.name.replace(/\[object Object\]/g, '');
      const newFile = new File([item], cleanedName, { type: item.type });
      this.files.push(newFile);
    }
    this.uploadFilesSimulator(0, files)


  }

  removeFile() {
    this.demoFile = []
    // this.imageArray = []
    // this.imageOutput = false
    this.files = []
    this.resetRadioButtons()
  }

  uploadFilesSimulator(index: number, files: any) {
    setTimeout(() => {
      if (index === this.files.length) {
        console.log("RETURN")
        return;
      } else {
        this.files[index].progress = 0;
        const progressInterval = setInterval(() => {
          if (this.files[index].progress >= 100) {
            clearInterval(progressInterval);
          } else {
            console.log("ELSE BLOCK")
            this.files[index].progress += 10;
          }
        }, 200);
      }
    }, 1000);
  }


  // submit call for the api

  submit() {
    if (this.form.invalid) {
      this.snackBar.open('Please select a File along with at least one of the Select type ', '✖', {
        horizontalPosition: 'center',
        verticalPosition: 'top',
        duration: 3000,
      });
      return;
    }
    console.log("submit")
    this.uploadFileData()
  }
  uploadFileData() {
    this.showSpinner1 = true;
    this.getLotDetails(this.user);
    // for (let i = 0; i < this.demoFile.length; i++) {
      const fileData = new FormData();
      this.selectedFile = this.files[0];
      fileData.append('file', this.selectedFile);
      fileData.append('userId', this.user)
      fileData.append('tenant', this.tenantarr)
      this.workBenchPostApiCall(fileData)
    // }
  }

  intervalId: any
  workBenchPostApiCall(fileData: any) 
  {
    // let i = 0
    // this.intervalId = setInterval(() => {
    //   if (i == 5) {
    //     clearInterval(this.intervalId);
    //   }
    //   i++
    //   this.getLotDetails(this.user)
    // }, 5000);


    // this.https.post(this.workBenchPostApi,fileData).subscribe((res) =>{
    this.https.post(this.Workbench_UploadFile, fileData).subscribe((res) => {
      // this.edited = true;
      // anonymize
      console.log("inside analyze=====", res)
      // update table
      this.showSpinner1 = false
      clearInterval(this.intervalId);
      this.getLotDetails(this.user);
    }, error => {
      this.showSpinner1 = false;
      const message = (error && error.error && (error.error.detail || error.error.message)) || "The Api has failed"
      const action = "Close"
      this.snackBar.open(message, action, {
        duration: 3000,
        panelClass: ['le-u-bg-black'],
      });
    }
      // , error => {
      //   // You can access status:
      //   console.log(error.status);
      //   if (error.status == 430) {
      //     this.showSpinner1 = false;
      //     this.edited = false;
      //     console.log(error.error.detail)
      //     console.log(error)
      //     const message = error.error.detail
      //     const action = "Close"
      //     this._snackBar.open(message, action, {
      //       duration: 3000,
      //       panelClass: ['le-u-bg-black'],
      //     });
      //   } else {
      //     this.showSpinner1 = false;
      //     this.edited = false;
      //     // console.log(error.error.detail)
      //     console.log(error)
      //     const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
      //     const action = "Close"
      //     this._snackBar.open(message, action, {
      //       duration: 3000,
      //       panelClass: ['le-u-bg-black'],
      //     });

      //   }
      // }
    )


  }

  viewoptions() {
    // console.log("Array===",this.selectedOptions)
    // [Privacy: true, Profanity: true, Explainability: true, FM-Moderation: true]
    const myObject = { ...this.selectedOptions };
    console.log("myObject===", myObject)
    const filteredKeys = this.filterKeysByBoolean(myObject);
    console.log("only keys", filteredKeys);
    this.tenantarr = filteredKeys

    this.form.patchValue({
      options: this.tenantarr
    });

  }
  filterKeysByBoolean(obj: Record<string, boolean>): string[] {
    return Object.keys(obj).filter((key) => obj[key]);
  }
  isCompleted(data: any): boolean {
    if (data == "Completed") {
      return true
    }
    else {
      return false
    }

  }

  sampleSrc1 = environment.imagePathurl + '/assets/image/csvIcon2.png';
  sampleFile1 = environment.imagePathurl + '/assets/samplefiles/Sample_File1.csv';
  sampleFile2 = environment.imagePathurl + '/assets/samplefiles/Sample_File2.csv';
  // sampleSrc2 = environment.imagePathurl + '/assets/image/sampleImage2.png';
  // sampleSrc3 = environment.imagePathurl + '/assets/image/sampleImage3.jpg';

  onClick(s: any) {
    console.log("s======",s);
    fetch(s)
      .then((response) => response.blob())
      .then((blob) => {
        const file = new File(
          [blob],
          s.replace(/^.*[\\\/]/, { type: 'csv' })
        );
        const abc: any = [];
        abc.push(file);
        // this.imgBrowseHandler(file)
        // console.log("conver6ec file ", file);
        this.selectedFile = file;
        // this.files.push(file)
        this.prepareFilesList(abc);

        this.demoFile.push(file);
        this.form.get('file')?.setValue('validFileValue');

        // this.demoFilesLenght = this.demoFile.length
        // this.cdr.detectChanges();
      })
      .catch((error) => {
      });

    //  This works in standalone but not in MFE

    //  this.getImage(s).subscribe(response =>{
    //   this.selectedFile=response;
    //   this.demoFile.push(response)

    //   console.log(this.demoFile)
    //   //console.log("length check demo:"+this.selectedFile.length)
    //    //console.log("rsponce"+response.size)
    //   this.demoFilesLenght =response.size
    //  }
    //   )

    // this.cdr.detectChanges();
  }

  viewchange() {
    console.log('view change', this.favoriteSeason);
  }

  resetRadioButtons() {
    this.favoriteSeason = null; // or any default value that doesn't match the radio button values
  }




}
