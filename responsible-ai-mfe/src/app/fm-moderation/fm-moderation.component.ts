/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Component, OnChanges, SimpleChanges, OnDestroy, ViewEncapsulation, ViewChild } from '@angular/core';
import { FmModerationService } from '../services/fm-moderation.service';
import { catchError, map, throwError } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { RightSidePopupComponent } from './right-side-popup/right-side-popup.component';
import { MatDialog } from '@angular/material/dialog';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { RoleManagerService } from '../services/role-maganer.service';
import { SharedDataService } from '../services/shared-data.service';
import { NgbPopover } from '@ng-bootstrap/ng-bootstrap';
import { NgModel } from '@angular/forms';
import { ImageService } from '../image/image.service';
import { ImageDialogComponent } from '../image-dialog/image-dialog.component';
import { NonceService } from '../nonce.service';
import { UserValidationService } from '../services/user-validation.service';

@Component({
  selector: 'app-fm-moderation',
  templateUrl: './fm-moderation.component.html',
  styleUrls: ['./fm-moderation.component.css']
})
export class FmModerationComponent {
  // FOR SHIMMER EFFECT
  isLoadingSelectType = true;
  isLoadingPrompt = true;
  /////
  selectedAccount='';
  selectedPortfolio='';
  Placeholder:string = 'Enter Prompt (supports prompt with emojis also)'
  tempValue: number = 0;
  spinner = false;
  apiEndpoints: any = {}
  roles: any;
  roleMlChecked = false;
  tenantarr: any = []
  optionarr: any = []
  selectedOptions: any = []
  options: any = ["Privacy", "Profanity", "FM-Moderation", "Explainability", "Fairness"]
  selectUsecaseOptions: any = ["Demo", "Navi"]
  portfolioName: any ='';
  accountName: any = '';
  exclusionList: any
  roleML: boolean = false;
  loggedINuserId: any;
  userRoleSettings: any = {
    openAiStatusasperUserRole: '',
    selfReminder: '',
    llmInteraction: '',
    // isNemo:''
  };
  llmBased: any = [];
  selectCoveComplexity: any = 'simple';
  selectPromptTemplate: any = 'GoalPriority';
  uncertainitySwitchCheck: boolean = false;
  hallucinationSwitchCheck: boolean = false;
  nemoGaurdrailCheck: boolean = false;
  noOfOptionUncertanity: number = 2;
  selectedLlmModel: any = 'gpt4';
  selectedTranslate: any = 'no';
  activeTab = '';
  buttonText: string = 'Execute Local FM Moderation';
  fmlocalselected = false;
  submitFlag= false;
  optionFlag= false;
  coupledModeration= false;
  filePreview: any = '';
  explainabilityOption: string = 'LLM';
  fmTimeApiResult = {
    "OpenAIInteractionTime": '',
    "requestModeration": '',
    "responseModeration": ''
  }

  openAIRes = {}
  COTRes: any = {}
  THOTRes: any = {}
  privacyResponse: any = {};
  profanityRes: any = {};
  explainabilityRes: any = {};
  fairnessRes: any = {};
  coupledModerationRes: any = {};
  nemoModerationRailRes: any = {};
  privacyOption = 'Choose Options';
  panelOpenState = false;
  privacy_options = ["Privacy-Analyze", "Privacy-Anonymize", "Privacy-Encrypt", "Privacy-Highlight"];
  Language_options = ["en", "fr"]
  nemoChecksApiResponses: any = {};
  // covResponse: any = {finishReason:"stop",index:0,text:"Hello! Absolutely, I'm here to provide helpful, accurate, and responsible information. If you have any questions or need assistance with something, feel free to ask, and I'll do my best to assist you.","timetaken":2.031};
  covResponse: any;
  covState: any = {
    active: false,
    hallucination: false,
    payload: {}
  }
  cotState: any = {
    active: false,
    hallucination: false,
    payload: {}
  }
  thotState: any = {
    active: false,
    hallucination: false,
    payload: {}
  }
  tokenImpState: any = {
    active: false,
    payload: {}
  }
  gotState: any = {
    active: false,
    payload: {}
  }
  llmExplainState: any = {
    active: false,
    payload: {}
  }
  contentDetectorState: any = {
    active: false,
    propmt: ''
  }
  serperResponseState: any = {
    model: this.selectedLlmModel,
    payload: {}
  }
  files: any = [];
  filesExplainability: any = [];
  demoFile: any = [];
  demoFile1: any = [];
  ExplanabilityFileId: any;
  ExplanabilityFileName: any = '';
  file: any;
  allEmbeddingsRes: any = [];
  selectedEmbeddedFileName: any = '';
  selectedEmbeddedFileId: any;
  hallucinateRetrievalKeplerRes: any = {
    "status": false,
    "errorMesssage": '',
    "response": {}
  };
  gEvalres: any = {};
  hallucinationResModerationData: any = {};
  llmEvalRes: any = {
    selectedOption: '',
    response: []
  }
  prompt: any = '';
  llmEvalPayload: any = {
    "AccountName": "None",
    "PortfolioName": "None",
    "userid": "None",
    "lotNumber": 1,
    "Prompt": this.prompt,
    "model_name": this.selectedLlmModel,
    "temperature": this.tempValue,
    "PromptTemplate": this.selectPromptTemplate,
  }
  requestModerationTemplates: any = [];
  responseModerationTemplates: any = [];
  templateBasedPayload: any = {
    status: false,
  };
 RagMultimodal:any =["jpg","jpeg","png","gif","bmp","jfif" ];
 RagMultiVideo:any =["mp4","3gp"];
  RagMultiFiles:any=[];
  RagMultiModalResponse:any ={
    "status": false,
    "errorMessage": '',
    "response": {},
    "multiModal": false
  };

  fairnessEvaluator: any = 'GPT_4';
  useCaseSelectedFlag: boolean = false;
  selectedUseCaseName: any = '';
  setLoadTemplateResMod: boolean = false;
  allTemplates: any = [];
  changeTab(tab: string) {
    this.activeTab = tab;
  }
  setLoadTemplateResModTrue() {
    console.log("setLoadTemplateResModTrue")
    this.setLoadTemplateResMod = true
  }

  tooltipContent: any;
  // Explainability variables
  isLoadingCOV: boolean = false;
  private COVUrl:any;
  covFinalAnswer:any;
  finalAnswer: string = '';
  COVAnswer: string = '';
  ngAfterViewInit() {
    const tooltipDiv = document.getElementById('tooltip-content');
    if (tooltipDiv) {
      this.tooltipContent = tooltipDiv.innerHTML;
    }
  }
  // TETSING
  openRightSideModal(data: any) {
    const dialogRef = this.dialog.open(RightSidePopupComponent, {
      width: '52vw',
      height: 'calc(100vh - 57px)', // Subtract the height of the navbar
      position: {
        top: '57px', // Position the modal below the navbar
        right: '0'
      },
      data: data,
      backdropClass: 'custom-backdrop'
    });

    dialogRef.afterClosed().subscribe(() => {
      // this.getAllBatches()
      console.log("POPUP CLOSE")
    });
  }


  constructor(private imageService: ImageService, public roleService: RoleManagerService, private sharedDataService: SharedDataService, private sanitizer: DomSanitizer, private https: HttpClient, private fmService: FmModerationService, public _snackBar: MatSnackBar, public dialog: MatDialog,public nonceService:NonceService,private validationService:UserValidationService) { }
  ngOnInit(): void {

    this.roles = this.roleService.getLocalStoreUserRole()
    this.options = this.roleService.getSelectedTypeOptions("Workbench", "Unstructured-Text", "Generative-AI")
    // FOR HACKATHON
    this.settingSelectOptions();
    ////////////////////

    this.fmService.fetchApiUrl();

    this.CallGetTemplates();
    let { ip_port, Account_Role } = this.retrieveLocalStorageData();
    console.log(ip_port,"ip port to be sent")
    this.setApiList(ip_port);
    this.initializeUserRole(Account_Role);
    //isLoadingSelectType = false;

    // set timeout for is loading
    this.isLoadingSelectType = false;
    this.isLoadingPrompt = false;

    this.selectedNotification = 'None';
    this.callModerationGetTemplates();
    // // set localstorage localfm variable to false
    // localStorage.setItem('localfm', 'false');
  }

  callModerationGetTemplates() {
    this.fmService.moderationGetTemplates().subscribe(
      (res: any) => {
        console.log(res);
      },
      error => {
        console.log(error);
      });
  }

  // ngOnDestroy() {
  //   this.resetData();
  // }

  formatOption(option: string): string {
    return option.replace(/_/g, ' ');
  }

  // FOR HACKATHON ONLY
  settingSelectOptions() {
    if (this.roles == 'ROLE_ML') {
      this.options = ["FM-Moderation"]
      this.selectedOptions["FM-Moderation"] = true;
      this.roleMlChecked = true;
      this.viewoptions()
    }
    console.log(this.options, "OPTIONS IN FUNCTION")

  }
  //////////////////////////////
  viewoptions() {
    const myObject = { ...this.selectedOptions };
    console.log("myObject===", myObject)
    const filteredKeys = this.filterKeysByBoolean(myObject);
    console.log("only keys", filteredKeys);
    this.tenantarr = filteredKeys;
    if (this.tenantarr.includes('Fairness') && this.filesMultiModel.length > 0) {
      this.Placeholder = "Enter Context"
    }else {
      this.Placeholder = "Enter Prompt";
    }
    if(!(this.tenantarr.includes('FM-Moderation'))){
      this.hallucinationSwitchCheck = false; // file upload needs to be reset if fm not in list
      this.coupledModeration = false;
    }
    if((this.tenantarr.includes('FM-Moderation'))){
      this.coupledModeration = true;
    }
  }
  filterKeysByBoolean(obj: Record<string, boolean>): string[] {
    return Object.keys(obj).filter((key) => obj[key]);
  }
  setApiList(ip_port: any) {
    // MULTIMODEL
    this.privAnonImgUrl2 = ip_port.result.Privacy + ip_port.result.Privacy_image_anonymize;
    this.privAnzImgUrl2 = ip_port.result.Privacy + ip_port.result.Privacy_image_analyze;
    this.profImageAnalyse = ip_port.result.Profanity + ip_port.result.Profan_Image_Analyse;
    this.fairness_image = ip_port.result.FairnessAzure + ip_port.result.FairnessImage;
    this.apiEndpoints.multimodal = ip_port.result.FM_Moderation + ip_port.result.Multimodel;

    this.apiEndpoints.fm_api = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_completions; // + environment.fm_api
    this.apiEndpoints.fm_api_openAi = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_openai; //+ environment.fm_api_openAi
    this.apiEndpoints.llm_eval = ip_port.result.FM_Moderation + ip_port.result.EvalLLM;
    // this.fm_api_privacyShield = this.ip_port.result.FM_Moderation + this.ip_port.result.Moderationlayer_PrivacyPopup; //+ environment.fm_api_privacyShield
    // this.priAnonApiUrl2 = this.ip_port.result.FM_Moderation + this.ip_port.result.Privacy_text_anonymize; //+ environment.priAnonApiUrl2
    this.apiEndpoints.fm_api_time = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_ModerationTime; //+ environment.fm_api_time
    // this.fm_api_inf_ProfanityPopup = this.ip_port.result.FM_Moderation + this.ip_port.result.Moderationlayer_ProfanityPopup; // + environment.fm_api_inf_ProfanityPopup
    // this.fm_api_inf_ToxicityPopup = this.ip_port.result.FM_Moderation + this.ip_port.result.Moderationlayer_ToxicityPopup; // + environment.fm_api_inf_ToxicityPopup
    this.apiEndpoints.admin_fm_admin_UserRole = ip_port.result.Admin + ip_port.result.Admin_userRole; // + environment.admin_fm_admin_UserRole
    this.apiEndpoints.nemo_TopicalRail = ip_port.result.Nemo + ip_port.result.Nemo_TopicalRail; //+ environment.nemo_TopicalRail
    this.apiEndpoints.nemo_JailBreakRail = ip_port.result.Nemo + ip_port.result.Nemo_JailBreakRail; // + environment.nemo_JailBreakRail
    this.apiEndpoints.nemo_ModerationRail = ip_port.result.Nemo + ip_port.result.Nemo_ModerationRail; // + environment.nemo_ModerationRail
    this.apiEndpoints.nemo_FactCheckRail = ip_port.result.Nemo + ip_port.result.Nemo_FactCheckRail; // + environment.nemo_FactCheckRail
    this.apiEndpoints.rag_Retrieval = ip_port.result.Rag + ip_port.result.RAG_RetrievalKepler;//'http://10.68.44.81:8002/rag/v1/RetrievalKepler'; // + environment.rag_Retrieval
    // this.Moderationlayer_feedback = this.ip_port.result.FM_Moderation + this.ip_port.result.Moderationlayer_feedback;
    this.apiEndpoints.Moderationlayer_COV = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_COV;
    this.apiEndpoints.Moderationlayer_openaiCOT = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_openaiCOT;
    this.apiEndpoints.Moderationlayer_gEval = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_gEval;
    this.apiEndpoints.RAG_gEval = ip_port.result.Rag + ip_port.result.RagGEVAL;
    this.apiEndpoints.Moderationlayer_Translate = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_Translate;
    this.apiEndpoints.fm_config_getAttributes = ip_port.result.Admin + ip_port.result.Fm_Config_GetAttributes;
    // //this.fm_config_getAttributes = "http://localhost:30016/api/v1/rai/admin/getAttributes"
    // this.hall_cov = this.ip_port.result.Rag + this.ip_port.result.RagCOV;
    // this.hall_cot = this.ip_port.result.Rag + this.ip_port.result.RagCOT;//"http://10.68.44.81:8002/rag/v1/cot";
    this.apiEndpoints.tokenImp = ip_port.result.Llm_Explain + ip_port.result.Token_Importance;
    this.apiEndpoints.UncertainApi = ip_port.result.Llm_Explain + ip_port.result.Uncertainty;
    this.apiEndpoints.thotApi = ip_port.result.FM_Moderation + ip_port.result.OpenAiThot;

    // PRIVACY API
    this.apiEndpoints.privacyAnonApi = ip_port.result.Privacy + ip_port.result.Privacy_text_anonymize;
    this.apiEndpoints.privacyAnalyzeApi = ip_port.result.Privacy + ip_port.result.Privacy_text_analyze;
    this.apiEndpoints.privacyEncrypt = ip_port.result.Privacy + ip_port.result.Privacy_encrypt;
    this.apiEndpoints.privacyDecrypt = ip_port.result.Privacy + ip_port.result.Privacy_decrypt;

    // PROFANITY API
    this.apiEndpoints.profAnzApiUrl = ip_port.result.Profanity + ip_port.result.Profanity_text_analyze  // +  environment.profAnzApiUrl
    this.apiEndpoints.profCenApiUrl = ip_port.result.Profanity + ip_port.result.Profanity_text_censor
    // Explainability API
    this.apiEndpoints.explApiUrl = ip_port.result.Explainability;
    this.COVUrl = ip_port.result.FM_Moderation + ip_port.result.Moderationlayer_COV;

    // FAIRNESS API
    this.apiEndpoints.FairnessApiUrl = ip_port.result.FairnessAzure + ip_port.result.FairUnstructure;
    // HALLUCINATION
    this.apiEndpoints.Admin_getEmbedings = ip_port.result.Admin_Rag + ip_port.result.Admin_getEmbedings;
    this.apiEndpoints.rag_FileUpload = ip_port.result.Rag + ip_port.result.RAG_FileUpload
    this.apiEndpoints.hall_cov = ip_port.result.Rag + ip_port.result.RagCOV;
    this.apiEndpoints.hall_cot = ip_port.result.Rag + ip_port.result.RagCOT;//"http://10.68.44.81:8002/rag/v1/cot";
    this.apiEndpoints.hall_thot = ip_port.result.Rag + ip_port.result.RagTHOT;
    // RAG MULTIMODAL
    this.apiEndpoints.rag_image = ip_port.result.Rag + ip_port.result.Rag_Image;
    this.apiEndpoints.rag_video = ip_port.result.Rag + ip_port.result.Rag_Video;

  }
  retrieveLocalStorageData() {
    let ip_port;
    let Account_Role;
    if (localStorage.getItem('role') != null) {
      const role = localStorage.getItem('role');
      if (JSON.parse(role!) == 'ROLE_ML') {
        this.roleML = true;
      }
    }
    if (localStorage.getItem('res') != null) {
      const x = localStorage.getItem('res');
      if (x != null) {
        ip_port = JSON.parse(x);
      }
    }
    if (localStorage.getItem('role') != null) {
      const x = localStorage.getItem('role');
      if (x != null) {
        Account_Role = JSON.parse(x);
        console.log(' Account_Role', Account_Role);
      }
    }
    
    if (window && window.localStorage && typeof localStorage !== 'undefined') {
      const x = localStorage.getItem("userid") ? JSON.parse(localStorage.getItem("userid")!) : "NA";
      if (x != null && (this.validationService.isValidEmail(x) || this.validationService.isValidName(x))) {
        this.loggedINuserId = x
        console.log(" userId", this.loggedINuserId)
      }
    }
    return { ip_port, Account_Role };
  }
  initializeUserRole(Account_Role: any) {
    this.https.post(this.apiEndpoints.admin_fm_admin_UserRole, { role: Account_Role }).subscribe(
      (res: any) => {
        this.userRoleSettings.openAiStatusasperUserRole = res.isOpenAI;
        this.userRoleSettings.selfReminder = res.selfReminder;
        // this.userRoleSettings.isNemo = res.isNemo;
        this.userRoleSettings.llmInteraction = res.isOpenAI ? 'yes' : 'no';
        console.log(this.userRoleSettings)
      },
      error => {
        console.log(error.status);
        if (error.status == 430) {
          // this.showSpinner1 = false;
          // this.edited = false;
          console.log(error.error.detail);
          console.log(error);
          const message = error.error.detail;
          const action = 'Close';
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
        } else {
          // this.showSpinner1 = false;
          // this.edited = false;
          // console.log(error.error.detail)
          console.log(error);
          let message
          if (error.status === 500) {
            message = "Internal Server Error. Please try again later.";
          } else {
            message = error.error.detail || error.error.message || "API has failed";
          }
          const action = 'Close';
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
        }
      });
  }

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 3000,
      panelClass: ['le-u-bg-black'],
    });
  }

  isEmptyObject(obj: Object): boolean {
    return JSON.stringify(obj) === '{}';
  }

  // changeApiUrls() {
  //   // Check the current value of 'localfm'
  //   if (localStorage.getItem('localfm') === 'true') {
  //     // If 'localfm' is true, set it to false and change the button text
  //     localStorage.setItem('localfm', 'false');
  //     this.buttonText = 'Switch to Local FM';
  //   } else {
  //     // If 'localfm' is false or null, set it to true and change the button text
  //     localStorage.setItem('localfm', 'true');
  //     this.buttonText = 'Switch Deployed FM';
  //   }

  //   // Print 'localfm'
  //   console.log(localStorage.getItem('localfm'));


  // }
  selectEmbeddedMethod(data: any) {
    this.files = []
    this.RagMultiFiles=[];
    let selectedOption = data.options[data.options.selectedIndex];
    this.selectedEmbeddedFileName = selectedOption.value;
    this.selectedEmbeddedFileId = selectedOption.id;
    // console.log(data.value)
    // console.log(data.id)
    // this.selectedEmbeddedFileName = data.value
    // this.selectedEmbeddedFileId = data.id
    // console.log(this.selectedEmbeddedFileId,this.selectedEmbeddedFileId)
  }
  SettingValue():void {
    this.fmlocalselected = true;
  }

  onSubmit(formData: any) {
    this.getSelectedValues();
    if (this.tenantarr == undefined || this.tenantarr.length == 0) {
      const message = 'Please select Select Type';
      const action = 'Close';
      this._snackBar.open(message, action, {
        duration: 3000,
        horizontalPosition: 'left',
        panelClass: ['le-u-bg-black'],
      });
      return;
    }
    if (this.tenantarr.includes('Fairness') && this.fairnessEvaluator.length == 0) {
      const message = 'Please select Evaluator for fairness';
      const action = 'Close';
      this._snackBar.open(message, action, {
        duration: 3000,
        horizontalPosition: 'left',
        panelClass: ['le-u-bg-black'],
      });
      return;
    }

    this.optionarr= this.tenantarr;
    this.optionFlag= true;
    if((this.tenantarr.includes('FM-Moderation'))){
      this.coupledModeration = true;
      this.submitFlag = true
    }else{
      this.submitFlag = false
    }

    // Rempoving the template Bsased Responses from Service
    this.sharedDataService.clearResponses();
    this.setLoadTemplateResMod = false;
   // this.templateBasedPayload['status'] = false;

   let { hallucinationSwitch, nemoGaurdrail, selectedUsecase, prompt, temp, llmAsEvaluatorSwitch } = formData.value;
   let accountName = this.selectedAccount;
   let portfolioName = this.selectedPortfolio;
    this.prompt = prompt;
    this.selectedUseCaseName = selectedUsecase;
    // this.resetMultiModelResult()
    this.resetResultData()
    // MULTIMODEL
    if (this.tenantarr.includes('FM-Moderation') && this.filesMultiModel.length > 0) {
      this.callMultiModel()
    }

    // text based templates checks 
    if (selectedUsecase == '' || selectedUsecase == 'Navi') {
      if (this.filesMultiModel.length > 0) {
        this.requestModerationTemplates = ["Prompt Injection Check", "Jailbreak Check","Language Critique Coherence Check", "Language Critique Fluency Check", "Language Critique Grammar Check", "Language Critique Politeness Check"]
        
      } else {
        this.requestModerationTemplates = ["Prompt Injection Check", "Jailbreak Check", "Fairness and Bias Check", "Language Critique Coherence Check", "Language Critique Fluency Check", "Language Critique Grammar Check", "Language Critique Politeness Check"] //imp
        

      }
      this.responseModerationTemplates = ["Response Completeness Check", "Response Conciseness Check", "Response Language Critique Coherence Check", "Response Language Critique Fluency Check", "Response Language Critique Grammar Check", "Response Language Critique Politeness Check"]
      this.templateBasedPayload.userid = this.loggedINuserId
      if (selectedUsecase == 'Navi') {
        this.callEvalLLMNavi(prompt, 'Navi Tone Correctness Check');
      }
    }

    if (this.tenantarr.includes('FM-Moderation') && hallucinationSwitch && this.selectedEmbeddedFileName == '' && this.files[0] == undefined) {
      const message = 'Please select the embeddings or upload the file';
      const action = 'Close';
      this._snackBar.open(message, action, {
        duration: 3000,
        horizontalPosition: 'left',
        panelClass: ['le-u-bg-black'],
      });
      return;
    }
    this.llmEvalPayload = {
      "AccountName": accountName,
      "PortfolioName": portfolioName,
      "userid": "None",
      "lotNumber": 1,
      "Prompt": this.prompt,
      "model_name": this.selectedLlmModel,
      "temperature": this.tempValue,
      "PromptTemplate": this.selectPromptTemplate,
    }

    if (!prompt || !prompt.trim()) {
      const message = 'Please enter the prompt';
      const action = 'Close';
      this._snackBar.open(message, action, {
        duration: 3000,
        horizontalPosition: 'left',
        panelClass: ['le-u-bg-black'],
      });
      return;
    }


    this.spinner = true;
    this.changeTab('');
    this.privacyResponse = {};
    this.profanityRes = {};
    this.explainabilityRes = {};
    this.coupledModerationRes = {};
    if (this.tenantarr.includes('Privacy')) {
      let { exclusionListPrivacy, fakeDataFlag } = formData.value;
      let accountNamePrivacy = this.selectedAccount;
      let portfolioNamePrivacy = this.selectedPortfolio;
      this.callPrivacyAPI(prompt, accountNamePrivacy, portfolioNamePrivacy, exclusionListPrivacy, fakeDataFlag);
    }
    if (this.tenantarr.includes('Profanity')) {
      console.log("insafety")
    let { exclusionListProf } = formData.value;
    let accountNameProf = this.selectedAccount;
    let portfolioNameProf = this.selectedPortfolio;
      this.callProfanityAPI(prompt);
    }
    if (this.tenantarr.includes('Explainability')) {
      this.callExplainabilityAPI(prompt);
    }
    if (this.tenantarr.includes('Fairness')) {
      if (this.filesMultiModel.length > 0) {
        const formPayload = new FormData();
        formPayload.append('prompt', this.prompt);
        formPayload.append('evaluator', "GPT_4o");
        formPayload.append('image', this.filesMultiModel[0]);
        this.fairnessImage(formPayload)
      } else {
        this.callFairnessAPI(prompt);
      }
    }
    if (this.tenantarr.includes('FM-Moderation')) {
      // HANDLE IF PROMPT ENPTY OR numDesc <0 or > 2 ----------- HAVE TO IMPLEMENT
      temp = (temp / 10).toFixed(1);
      let tempStringValue = temp.toString();
    if (tempStringValue == '0.0') {
        tempStringValue = '0';
      }
      if (llmAsEvaluatorSwitch) {
        this.llmBased = ["randomNoiseCheck"];
      } else {
        this.llmBased = [];
      }
      this.serperResponseState = {
        model: this.selectedLlmModel,
        payload: {
          inputPrompt: prompt
        }
      }

      // CHECK textArr.length 0 or not --------------------HAVE TO IMPLEMENT
      if (portfolioName.length == 0 || accountName.length == 0) {
        if (!hallucinationSwitch) {
          console.log("hallucinationSwitch is false");
          if (!this.userRoleSettings.openAiStatusasperUserRole) { //-------------IF OPENAI IS FALSE----------------
            this.callFMApi(prompt, tempStringValue, nemoGaurdrail, hallucinationSwitch);
          } else if (this.userRoleSettings.openAiStatusasperUserRole) {
            this.callFMApi(prompt, tempStringValue, nemoGaurdrail, hallucinationSwitch)
            if (!this.roleML) {
              // this.covgetApi(prompt);
              this.covState = {
                active: this.useCaseSelectedFlag ? false : true,
                payload: {
                  text: prompt,
                  complexity: this.selectCoveComplexity,
                  model_name: this.selectedLlmModel
                }
              }
              console.log("covState", this.covState)
              this.cotState = {
                active: this.useCaseSelectedFlag ? false : true,
                payload: {
                  temperature: tempStringValue,
                  Prompt: prompt,
                  model_name: this.selectedLlmModel
                }
              }
              this.thotState = {
                active: this.useCaseSelectedFlag ? false : true,
                payload: {
                  temperature: tempStringValue,
                  Prompt: prompt,
                  model_name: this.selectedLlmModel
                }
              }
              // this.openAicotgetApi(prompt, tempStringValue);
              // this.openAiTHOTApi(prompt, tempStringValue)
            }
            this.callOpenAiApi(prompt, tempStringValue)
          }

        } else if (hallucinationSwitch) {
          this.callFMApi(prompt, tempStringValue, nemoGaurdrail, hallucinationSwitch);
          this.callOpenAiApi(prompt, tempStringValue)
        }
        if (nemoGaurdrail) {
          const fileData = new FormData();
          fileData.append('text', prompt);
          this.callNemoCheckApi(this.apiEndpoints.nemo_TopicalRail, fileData, 'nemoTopicalRailStatus', 'nemoTopicalRailTime');
          this.callNemoCheckApi(this.apiEndpoints.nemo_JailBreakRail, fileData, 'nemoJailbreakCheckStatus', 'nemoJailbreakCheckTime');
          this.callNemoCheckApi(this.apiEndpoints.nemo_FactCheckRail, fileData, 'nemoFactcheckRailStatus', 'nemoFactcheckRailTime');
        }
      } else {

        // if (this.hallucination == true) {
        //   // this.resetHall()
        //   // this.cdr.detectChanges();
        //   this.LLMinteractionValue = 'No';
        // }
        // get attributes based on account/portfolio
        const configPayload = {
          AccountName: accountName,
          PortfolioName: portfolioName,
        };
        this.callFMConfigApi(configPayload, accountName, portfolioName, tempStringValue, prompt).subscribe(
          ({ response, comp_Payload }) => {
            console.log(response);
            if (!hallucinationSwitch) {
              console.log("hallucinationSwitch is false");
              if (!this.userRoleSettings.openAiStatusasperUserRole) { //-------------IF OPENAI IS FALSE----------------
                this.callFMApi(prompt, tempStringValue, nemoGaurdrail, hallucinationSwitch, comp_Payload);
              } else if (this.userRoleSettings.openAiStatusasperUserRole) {
                this.callFMApi(prompt, tempStringValue, nemoGaurdrail, hallucinationSwitch, comp_Payload)
                if (!this.roleML) {
                  this.covState = {
                    active: this.useCaseSelectedFlag ? false : true,
                    payload: {
                      text: prompt,
                      complexity: this.selectCoveComplexity,
                      model_name: this.selectedLlmModel
                    }
                  }
                  console.log("covState", this.covState)
                  this.cotState = {
                    active: this.useCaseSelectedFlag ? false : true,
                    payload: {
                      temperature: tempStringValue,
                      Prompt: prompt,
                      model_name: this.selectedLlmModel
                    }
                  }
                  this.thotState = {
                    active: this.useCaseSelectedFlag ? false : true,
                    payload: {
                      temperature: tempStringValue,
                      Prompt: prompt,
                      model_name: this.selectedLlmModel
                    }
                  }
                }
                this.callOpenAiApi(prompt, tempStringValue)
              }
            } else if (hallucinationSwitch) {
              this.callFMApi(prompt, tempStringValue, nemoGaurdrail, hallucinationSwitch);
              this.callOpenAiApi(prompt, tempStringValue)
            }
          },
          error => {
            this.handleError(error);
          }
        );
      }
      if (!this.roleML) {
        this.tokenImpState = {
          active: this.useCaseSelectedFlag ? false : true,
          payload: {
            "inputPrompt": prompt,
            "modelName": "GPT"
          }
        }
        this.gotState = {
          active: this.useCaseSelectedFlag ? false : true,
          payload: {
            "inputPrompt": prompt,
            "modelName": 'gpt-35-turbo-16k'
          }
        }
        this.llmExplainState = {
          active: this.useCaseSelectedFlag ? false : true,
          payload: {
            "inputPrompt": prompt
          }
        }
        // Checking For Content Derector API
        const a = prompt.replace(/[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]/g, '');
        const words = a.split(' ');
        const filteredWords = words.filter((word: any) => word !== '');
        if (filteredWords.length >= 50) {
          this.contentDetectorState = {
            active: true,
            prompt: prompt
          }
        }
      }
    }
    this.fmlocalselected = false;
  }

  resetData(form: any) {
    this.hallucinationSwitchCheck = false;
    this.nemoGaurdrailCheck = false;
    this.files = [];
    this.RagMultiFiles=[];
    this.tState = false
    this.selectedTranslate = "no"
    this.selectedNotification = "no"
    this.selectedEmojiVal = "no"
    this.tLoading = false

    form.controls['prompt'].setValue('');
    form.controls['selectedUsecase'].setValue('');
    this.useCaseSelectedFlag = false;
    if (this.roles !== 'ROLE_ML') {
      console.log("ROLE_MLllllllllllllllll")
      this.selectedOptions = [];
      this.tenantarr = [];
    }
    this.spinner = false;
    this.removeFileMultimodel()
    this.resetResultData()
    this.optionarr= [];
    this.optionFlag= false;
  }

  resetResultData() {
    this.fmService.resetMultiModal();
    this.setLoadTemplateResMod = false;
    this.activeTab = ''
    this.privacyResponse = {};
    this.profanityRes = {};
    this.explainabilityRes = {};
    this.coupledModerationRes = {};
    this.fairnessRes = {};
    this.openAIRes = {};
    this.COTRes = {};
    this.THOTRes = {};
    this.nemoModerationRailRes = {};
    this.fmTimeApiResult.requestModeration = '';
    this.fmTimeApiResult.responseModeration = '';
    this.fmTimeApiResult.OpenAIInteractionTime = '';
    this.nemoChecksApiResponses = {};
    this.covResponse = {};
    this.covState = {
      active: false,
      hallucination: false,
      payload: {}
    }; console.log("covstate reseted");
    this.cotState = {
      active: false,
      hallucination: false,
      payload: {}
    }
    this.thotState = {
      active: false,
      hallucination: false,
      payload: {}
    }
    this.tokenImpState = {
      active: false,
      payload: {}
    }
    this.gotState = {
      active: false,
      payload: {}
    }
    this.llmExplainState = {
      active: false,
      payload: {}
    }
    this.contentDetectorState = {
      active: false,
      prompt: ''
    }
    this.serperResponseState = {
      model: this.selectedLlmModel,
      payload: {}
    }
    this.hallucinateRetrievalKeplerRes = {
      "status": false,
      "response": {}
    };
    this. RagMultiModalResponse ={
      "status": false,
      "response": {},
      "multiModal": false
    };
    this.gEvalres = {};
    this.hallucinationResModerationData = {};
    this.llmEvalRes = {
      selectedOption: '',
      response: []
    }
    this.templateBasedPayload.status = false;

    this.resetMultiModelResult()
  }

  requestTemplateGlobal=[]
  responseTemplateGlobal=[]
  globalMultiModeltemplateList:any = []
  globalMultiEvaltemplateList:any = []

  onTemplateSelect(event: any) {
    console.log(event?.target.value)
    console.log("all of the templates",this.allTemplates)

    if (event?.target.value != 'Navi') {
      let selectedTemplate = this.allTemplates.find((template: any) => template.mapId == event?.target.value);
      console.log("selectedTemplate", selectedTemplate)
      if (selectedTemplate.SingleModel) {// if contion for if single model is exists
        if (selectedTemplate.SingleModel && selectedTemplate.SingleModel.Template) {
          this.requestModerationTemplates = selectedTemplate.SingleModel.Template.requestTemplate;
          this.responseModerationTemplates = selectedTemplate.SingleModel.Template.responseTemplate;
          this.templateBasedPayload = {
            AccountName: selectedTemplate.account,
            PortfolioName: selectedTemplate.portfolio,
            userid: this.loggedINuserId
          }
        }else{
          this.requestModerationTemplates = [];
          this.requestModerationTemplates = [];
        }
        if (selectedTemplate.SingleModel && selectedTemplate.SingleModel.Model) {

          // this.requestTemplateGlobal = selectedTemplate.responseTemplate;
  
          this.requestTemplateGlobal = selectedTemplate.SingleModel.Model.requestTemplate;
          this.responseTemplateGlobal = selectedTemplate.SingleModel.Model.responseTemplate;
        }else{
          this.requestTemplateGlobal = [];
          this.responseTemplateGlobal = [];
        }

      }
      // if (selectedTemplate.MultiModel){
      //   // if it has multimodel values
      //   if (selectedTemplate.MultiModel && selectedTemplate.MultiModel.TextTemplate) {
      //     this.requestModerationTemplates = selectedTemplate.MultiModel.TextTemplate.requestTemplate;
      //     this.responseModerationTemplates = selectedTemplate.MultiModel.TextTemplate.responseTemplate;
      //     this.templateBasedPayload = {
      //       AccountName: selectedTemplate.account,
      //       PortfolioName: selectedTemplate.portfolio,
      //       userid: this.loggedINuserId
      //     }
      //   }else{
      //     this.requestModerationTemplates = [];
      //     this.requestModerationTemplates = [];
      //   }
      //   if (selectedTemplate.MultiModel && selectedTemplate.MultiModel.TextModel) {

      //     // this.requestTemplateGlobal = selectedTemplate.responseTemplate;
  
      //     this.requestTemplateGlobal = selectedTemplate.MultiModel.TextModel.requestTemplate;
      //     this.responseTemplateGlobal = selectedTemplate.MultiModel.TextModel.responseTemplate;
      //   }else{
      //     this.requestTemplateGlobal = [];
      //     this.responseTemplateGlobal = [];
      //   }
      //   if (selectedTemplate.MultiModel && selectedTemplate.MultiModel.ImageModel) {

      //     // this.requestTemplateGlobal = selectedTemplate.responseTemplate;
      //     // templateList
      //     this.globalMultiModeltemplateList= selectedTemplate.MultiModel.ImageModel.requestTemplate;
  
      //     // this.requestTemplateGlobal = selectedTemplate.MultiModel.TextModel.requestTemplate;
      //     // this.responseTemplateGlobal = selectedTemplate.MultiModel.TextModel.responseTemplate;
      //   }else{
      //     this.globalMultiModeltemplateList =[]
      //   }
      //   if (selectedTemplate.MultiModel && selectedTemplate.MultiModel.ImageTemplate) {

      //     // this.requestTemplateGlobal = selectedTemplate.responseTemplate;
      //     // templateList
      //     this.globalMultiEvaltemplateList= selectedTemplate.MultiModel.ImageTemplate.requestTemplate;
  
      //     // this.requestTemplateGlobal = selectedTemplate.MultiModel.TextModel.requestTemplate;
      //     // this.responseTemplateGlobal = selectedTemplate.MultiModel.TextModel.responseTemplate;
      //   }else{
      //     this.globalMultiEvaltemplateList =[]
      //   }
      // }
  }
    
    console.log("Template Based on Select Type", this.templateBasedPayload, this.requestModerationTemplates, this.responseModerationTemplates)
  }

  // -------------GET Initial Embeddings for Hallucination----------------
  getembeddigns() {
    const userIdvalue = this.loggedINuserId
    const body = new URLSearchParams();
    body.set('userId', userIdvalue.toString());
    this.https.post(this.apiEndpoints.Admin_getEmbedings, body, {
      headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
    }).subscribe(
      (res: any) => {
        this.allEmbeddingsRes = res;
        // this.dataSource1= res;
        // this.cacheId =  res[0].cacheId;
      }, error => {
        this.handleError(error);
      })
  }

  CallGetTemplates() {
    this.fmService.getTemplates().subscribe(
      (res: any) => {
        console.log(res)
        this.allTemplates = res?.accList;
      },
      error => {
        this.handleError(error);
      }
    )
  }

  // ----------Handle File Upload For Hallucination---------------------
  // fileBrowseHandler(imgFile: any) {
  //   this.selectedEmbeddedFileName = '';
  //   this.selectedEmbeddedFileId = '';
  //   this.prepareFilesList(imgFile.target.files);
  //   this.demoFile = this.files;
  //   this.file = this.files[0];
  // }
  fileBrowseHandler(imgFile: any) {
    this.selectedEmbeddedFileName = '';
    this.selectedEmbeddedFileId = '';
    this.demoFile = this.files;
    // this.browseFilesLenth = imgFile.target.files.length;
    // to validate file SAST
    const allowedTypes = ['application/pdf', 'text/csv', 'text/plain','image/jpg', 'image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/jfif'];
    for(let i =0; i< this.demoFile1.length; i++){
      if (!allowedTypes.includes(this.demoFile1[i].type)) {
        this._snackBar.open('Please upload valid file', 'Close', {
          duration: 2000,
        });
        this.demoFile1 = [];
        return ;
      }
    }
    this.prepareFilesList(imgFile.target.files);
    // console.log("Files[0]",this.files[0] )
    // const reader = new FileReader();
    // reader.readAsDataURL(this.files[0]);
    // reader.onload = (_event) => {
    //   this.filePreview = reader.result;
    //   console.log("filePreview",this.filePreview )
    // }
  }
  fileBrowseHandler1(imgFile: any) {
    this.ExplanabilityFileName = '';
    this.ExplanabilityFileId = '';
    this.demoFile1 = this.filesExplainability;
    // to validate file SAST
    const allowedTypes = ['application/pdf', 'text/csv', 'text/plain'];
    for(let i =0; i< this.demoFile1.length; i++){
      if (!allowedTypes.includes(this.demoFile1[i].type)) {
        this._snackBar.open('Please upload valid file', 'Close', {
          duration: 2000,
        });
        this.demoFile1 = [];
        return ;
      }
    }
    this.prepareFilesList1(imgFile.target.files);
    console.log("fileBrowseHandler", this.filesExplainability);
  }
  deleteFile(index: number) {
    if (this.files[index].progress < 100) {
      console.log("if of deltefile 1.");
      return;
    }
    console.log("in delete 1")
    this.files.splice(index, 1);
  }
  deleteFile1(index: number) {
    if (this.filesExplainability[index].progress < 100) {
      console.log("if of deltefile 1.");
      return;
    }
    console.log("in delete 1")
    this.filesExplainability.splice(index, 1);
  }

  // prepareFilesList(files: Array<any>) {
  //   this.files = [];
  //   this.demoFile = [];
  //   for (const item of files) {
  //     this.files.push(item);
  //   }
  //   this.uploadFilesSimulator(0, files)
  // }
  prepareFilesList(files: Array<any>) {
    for (const item of files) {
      item.progress = 0;
      const reader = new FileReader();
      reader.readAsDataURL(item);
      reader.onload = (_event) => {
          item.preview = reader.result;
          item.type = item.type;
      };
      console.log("item.preview", item.preview)
      console.log("item.type", item.type)
      this.files.push(item);
    }
    // this.fileDropEl.nativeElement.value = "";
    this.uploadFilesSimulator(0);
  }
  prepareFilesList1(filesExplainability: Array<any>) {
    for (const item of filesExplainability) {
      item.progress = 0;
      const reader = new FileReader();
      reader.readAsDataURL(item);
      reader.onload = (_event) => {
          item.preview = reader.result;
          item.type = item.type;
      };
      console.log("item.preview", item.preview)
      console.log("item.type", item.type)
      this.filesExplainability.push(item);
    }
    // this.fileDropEl.nativeElement.value = "";
    this.uploadFilesSimulator1(0);
    console.log("preparedfiles", this.filesExplainability)
  }


  uploadFilesSimulator(index: number) {
    setTimeout(() => {
      if (index === this.files.length) {
        return;
      } else {
        const progressInterval = setInterval(() => {
          if (this.files[index].progress === 100) {
            clearInterval(progressInterval);
            this.uploadFilesSimulator(index + 1);
          } else {
            this.files[index].progress += 20;
          }
        }, 200);
      }
    }, 1000);
  }

  uploadFilesSimulator1(index: number) {
    setTimeout(() => {
      if (index === this.filesExplainability.length) {
        return;
      } else {
        const progressInterval = setInterval(() => {
          if (this.filesExplainability[index].progress === 100) {
            clearInterval(progressInterval);
            this.uploadFilesSimulator1(index + 1);
          } else {
            this.filesExplainability[index].progress += 20;
          }
        }, 200);
      }
    }, 1000);
  }

  removeFile() {
    this.files = [];
    this.RagMultiFiles=[];
    this.demoFile = [];
    this.file = '';
    this.selectedEmbeddedFileName = '';
    this.selectedEmbeddedFileId = '';
    this.ExplanabilityFileName = '';
    this.ExplanabilityFileId = '';
  }

  //-----------------Upload Hallucination File------------------
  async callUploadEmbeddedFile() {
    const fileData = new FormData();
    for (let i = 0; i < this.demoFile.length; i++) {
      fileData.append('payload', this.demoFile[i]);
      console.log("new  file upload comp.........", fileData)
    }
    return new Promise((resolve, reject) => {
      this.https.post(this.apiEndpoints.rag_FileUpload, fileData).subscribe(
        (res: any) => {
          console.log("data sent to database" + res);
          this.selectedEmbeddedFileId = res;
          resolve(res);
        },
        error => {
          this.handleError(error);
          reject(error);
        }
      );
    });
  }
  async callUploadEmbeddedFile1() {
    const fileData = new FormData();
    for (let i = 0; i < this.demoFile1.length; i++) {
      fileData.append('payload', this.demoFile1[i]);
      console.log("new  file upload comp.........", fileData)
    }
    return new Promise((resolve, reject) => {
      this.https.post(this.apiEndpoints.rag_FileUpload, fileData).subscribe(
        (res: any) => {
          console.log("data sent to database" + res);
          this.ExplanabilityFileId = res;
          resolve(res);
        },
        error => {
          this.handleError(error);
          reject(error);
        }
      );
    });
  }
  checkRagMultiModal():any{ 
    this.RagMultiFiles = [];
    for (let i = 0; i < this.demoFile.length; i++) {
      const extension = (this.demoFile[i].name).split('.').pop();
      if (this.RagMultimodal.includes(extension.toLowerCase())){
        this.apiEndpoints.rag_multimodal = this.apiEndpoints.rag_image;
        this.RagMultiFiles.push(this.demoFile[i]);
        this.RagMultiModalResponse.multiModal = true;
      } else if (this.RagMultiVideo.includes(extension.toLowerCase()) ){
        this.apiEndpoints.rag_multimodal = this.apiEndpoints.rag_video;
        this.RagMultiFiles.push(this.demoFile[i]);
        this.RagMultiModalResponse.multiModal = true;
      }

      console.log("this.RagMultiFiles::",this.RagMultiFiles);
    }
    const res = this.RagMultiFiles.length > 0 ? true: false;
    return res;
  }
  async callMultimodalRag(){
    const fileData = new FormData();
    for (let i = 0; i < this.RagMultiFiles.length; i++) {
        fileData.append('file', this.RagMultiFiles[i]);
    }
    fileData.append('text',this.prompt);
    console.log("rag multi payload........", fileData)
    return new Promise((resolve, reject) => {
      this.https.post(this.apiEndpoints.rag_multimodal, fileData).subscribe(
        (res: any) => {
          this.RagMultiModalResponse.response.text = (res[0]?.replace(/\n\n/g, '<br>')).replace(/\n/g, '<br>');
          resolve(res);
        },
        error => {
          this.handleError(error);
          reject(error);
        }
      );
    });
  }
  removeRagFile(){
    this.RagMultiFiles = [];
  }
  resetExplainability() {
    this.activeTab = ''
    this.explainabilityRes = {};
    this.filesExplainability = [];
  }
  // ---------------CALLING APIS----------------------
  callEvalLLMNavi(prompt: any, templateName: any) {
    let payload = {
      Prompt: prompt,
      template_name: templateName,
      model_name: this.selectedLlmModel,
      AccountName: this.accountName ? this.accountName : "None",
      "PortfolioName": this.portfolioName ? this.portfolioName : "None",
      "userid": this.loggedINuserId,
      "lotNumber": 1,
      "Context": "None",
      "Concise_Context": "None",
      "Reranked_Context": "None",
      "temperature": this.tempValue,
      "PromptTemplate": this.selectPromptTemplate,
    }
    this.sharedDataService.updateNaviTonemoderationRes("status", 'LOADING');
    console.log(payload)
    this.https.post(this.apiEndpoints.llm_eval, payload).subscribe(
      (res: any) => {
        let response = res.moderationResults.response[0]
        this.sharedDataService.updateNaviTonemoderationRes("analysis", response.analysis);
        this.sharedDataService.updateNaviTonemoderationRes("context", response.Context);
        this.sharedDataService.updateNaviTonemoderationRes("sentiment", response.Sentiment);
        this.sharedDataService.updateNaviTonemoderationRes("domain", response.Domain);
        this.sharedDataService.updateNaviTonemoderationRes("toneScore", response['Tone Score']);
        this.sharedDataService.updateNaviTonemoderationRes("timetaken", response.timetaken);
        this.sharedDataService.updateNaviTonemoderationRes("status", 'COMPLETED');
      },
      error => {
        this.sharedDataService.updateNaviTonemoderationRes("status", 'FAILED');
        console.log(error);
      })
  }
  callPrivacyAPI(prompt: any, accountName: any, portfolioName: any, exclusionList: any, fakeDataFlag: any) {
    accountName = this.selectedAccount;
    portfolioName = this.selectedPortfolio;
    console.log("userloggedIN",this.loggedINuserId)
    let payloadAnon: any = {
      inputText: prompt,
      portfolio: portfolioName,
      account: accountName,
      exclusionList: exclusionList,
      user: this.loggedINuserId,
      fakeData: fakeDataFlag ? true : false,
      redactionType: "replace",
      piiEntitiesToBeRedacted: null as string[] | null,
      lotNumber:"1"
    
    };
 
    let payloadAnalyze: any = {
      inputText: prompt,
      portfolio: portfolioName,
      account: accountName,
      exclusionList: exclusionList,
      user: this.loggedINuserId,
      piiEntitiesToBeRedacted: null as string[] | null,
      nlp: null as string | null
    };    let payloadEncrypt = {
      inputText: prompt,
      portfolio: portfolioName,
      account: accountName,
      exclusionList: exclusionList,
      user: this.loggedINuserId,
      fakeData: fakeDataFlag ? true : false,
      redactionType: "replace",
      piiEntitiesToBeRedacted: null as string[] | null,
      lotNumber:"1"    };
    let payloadDecrypt = prompt;
    console.log("accountName::",accountName)
    if (accountName.length != 0 && portfolioName.length != 0) {
      payloadAnon = {
        inputText: prompt,
        portfolio: portfolioName,
        account: accountName,
        // IMPORTANT NEED TO ADD
        // exclusionList: desc.exclusion,
        exclusionList: exclusionList,
        user: this.loggedINuserId,
        fakeData: fakeDataFlag ? true : false,
        // fakeData: this.fakeDataStateValue, //IMPORTAMNT Slider
        "piiEntitiesToBeRedacted": [
        ],
        "redactionType": "replace"
      }
      payloadAnalyze = {
        inputText: prompt,
        portfolio: portfolioName,
        account: accountName,
        exclusionList: exclusionList,
        "piiEntitiesToBeRedacted": [
        ],
        //exclusionList: '',
 
        user: this.loggedINuserId
      }
    } else {
      payloadAnon.piiEntitiesToBeRedacted = []
      payloadAnon.portfolio = null;
      payloadAnon.account = null;
      //payloadAnon.nlp = this.nlpOption;
      payloadAnalyze.portfolio = null;
      payloadAnalyze.account = null;
      payloadAnalyze.piiEntitiesToBeRedacted = []
     // payloadAnalyze.nlp = this.nlpOption;
      payloadAnalyze.exclusionList = '';
      payloadAnon.user = this.loggedINuserId;
      payloadEncrypt.account =null;
      payloadEncrypt.portfolio =  null;

      
    
    }
 
    if (this.privacyOption == 'Choose Options') {
      this.callPrivacyAnalyze(payloadAnalyze);
      this.callPrivacyAnonymize(payloadAnon);
    } else if (this.privacyOption == 'Privacy-Analyze') {
      this.callPrivacyAnalyze(payloadAnalyze);
    } else if (this.privacyOption == 'Privacy-Anonymize') {
      this.callPrivacyAnonymize(payloadAnon);
    } else if (this.privacyOption == 'Privacy-Encrypt') {
      this.callPrivacyEncrypt(payloadEncrypt);
    } else if (this.privacyOption == 'Privacy-Highlight') {
      this.callPrivacyAnalyze(payloadAnalyze);
    }
  }
    // else if(this.privacyOption == 'Privacy-Decrypt'){
    //   this.callPrivacyDecrypt(payloadDecrypt);
    // }/// privacy decrypt api is being directly called after encrypt api response is recived
  resetPrivacyResult() {
    this.privacyResponse = {};
  }
  callProfanityAPI(prompt: any) {
    let payload = {
      inputText: prompt,
      user: this.loggedINuserId
    }
    this.https.post(this.apiEndpoints.profAnzApiUrl, payload).subscribe((res: any) => {
      console.log(res)
      this.profanityRes.AnazRes = res
    }
      , error => {
        this.handleError(error);
      })
    this.https.post(this.apiEndpoints.profCenApiUrl, payload).subscribe((res: any) => {
      console.log(res)
      this.profanityRes.cenRes = res
      this.spinner = false;
      if (this.activeTab == '') {
        this.changeTab('Profanity');
      }
    }
      , error => {
        this.handleError(error);
      })
  }
  callExplainabilityAPI(prompt: any) {
    if (this.explainabilityOption == 'Sentiment') {
       this.https.post(this.apiEndpoints.explApiUrl, { inputPrompt: prompt }).subscribe((expRes) => {
      this.explainabilityRes = expRes;
      console.log(expRes)
      this.spinner = false;
      if (this.activeTab == '') {
        this.changeTab('Explainability');
      }
    }, error => {
      this.handleError(error);
    })
    }
   else if (this.explainabilityOption == 'RAG') {
      this.callUploadEmbeddedFile1().then(res => {
        console.log(res);
        console.log(this.ExplanabilityFileId, "ExplanabilityFileId");
        this.spinner = false;
      if (this.activeTab == '') {
        this.changeTab('Explainability');
      }
      });
    } else {
      this.isLoadingCOV = true;
      const payload = {
        complexity: 'simple',
        model_name: 'gpt4',
        translate: this.selectedTranslate,
        text: this.prompt
      };
      if (this.activeTab == '') {
        this.changeTab('Explainability');
      }
      this.https.post(this.COVUrl, payload)
      .subscribe((response: any) => {
        this.spinner = false;
        
        console.log('API response:', response);
        this.covFinalAnswer = response.final_answer;
        this.finalAnswer = this.covFinalAnswer;
        let formattedText = response.verification_answers
        .replace(/Question: 1/, 'Question: 1')
        .replace(/Question: 2/, '<br><br>Question: 2')
        .replace(/Question: 3/, '<br><br>Question: 3')
        .replace(/Question: 4/, '<br><br>Question: 4')
        .replace(/Question: 5/, '<br><br>Question: 5')
        .replace(/Answer:/g, '<br>Answer:');
        this.COVAnswer = formattedText;
        this.isLoadingCOV = false;
      }, error => {
        this.isLoadingCOV = false;
      });
    }


  }
  callFairnessAPI(prompt: any) {
    console.log("in fariness api function")
    let body = new URLSearchParams();
    body.set('response', prompt.toString());
    body.set('evaluator', this.fairnessEvaluator.toString());
    this.https.post(this.apiEndpoints.FairnessApiUrl, body, {
      headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
    }).subscribe((fairRes) => {
      this.fairnessRes = fairRes
      console.log(fairRes)
      this.spinner = false;
      if (this.activeTab == '') {
        this.changeTab('Fairness');
      }
    }, error => {
      this.handleError(error);
    })
  }
  callFMApi(prompt: string, tempStringValue: string, nemoGaurdrail: any, hallucinationSwitch: any, payload?: any, hallucinationPostCall: any = false) {
    console.log("callFMApi");
    let data = payload ? payload : this.comp_Payload(prompt, tempStringValue, this.userRoleSettings.llmInteraction, this.selectPromptTemplate);
    // this.fmService.getFMService(this.apiEndpoints.fm_api, data)?.subscribe()
    // Define the Authorization
   
    // this.fmService.getFMService(this.apiEndpoints.fm_api, data, this.fmlocalselected, {})?.subscribe(
    this.fmService.getFMService(this.apiEndpoints.fm_api, data,this.fmlocalselected)?.subscribe(
        async (res: any) => {
          this.templateBasedPayload['status'] = true;
          // this.handle_FM_API_Response(res);
          if (hallucinationPostCall) {
            console.log("CALL FM API ---------------------------------------hallucinationPostCall=TRUE ")
            this.hallucinationResModerationData = res.moderationResults.requestModeration;
            console.log(this.hallucinationResModerationData)
          } else {
            console.log("CALL FM API ---------------------------------------hallucinationPostCall=FALSE")
            this.coupledModerationRes = res;
            this.coupledModeration= true;
            this.fmService.updateData(res);
            this.changeTab('Request Moderation');
          }
          let summaryStatus = res.moderationResults.requestModeration.summary.status;
          let reSstatus = res.moderationResults.responseModeration.summary.status;
          console.log("summaryStatus", summaryStatus)
          console.log("reSstatus", reSstatus)
          this.callNemoApi(prompt, nemoGaurdrail, summaryStatus);
          this.callFMTimeApi(hallucinationPostCall);
          this.spinner = false;
          // this.isCollapsed = true; // Collapse Right Panel

          if (hallucinationSwitch && !hallucinationPostCall) {
            if (summaryStatus == 'PASSED' || reSstatus == 'PASSED') {
              this.hallucinateRetrievalKeplerRes.status = true;
              if (this.files[0] != undefined) {
                if(!this.checkRagMultiModal()){
                this.callUploadEmbeddedFile().then(res => {
                  console.log(res)
                  if (res != null) {
                    console.log(this.selectedEmbeddedFileId, "selectedEmbeddedFileId")
                    const requestBody = {
                      fileupload: this.files.length == 0 ? false : true,
                      text: prompt,
                      vectorestoreid: this.selectedEmbeddedFileId.id,
                    }
                    const ragCov = {
                      fileupload: this.files.length == 0 ? false : true,
                      text: prompt,
                      vectorestoreid: this.selectedEmbeddedFileId.id,
                      complexity: this.selectCoveComplexity
                    }
                    this.hallucinateRetrievalKepler(requestBody, prompt, tempStringValue, nemoGaurdrail, summaryStatus);
                    this.cotState = {
                      active: this.useCaseSelectedFlag ? false : true,
                      hallucination: true,
                      payload: requestBody
                    }
                    this.thotState = {
                      active: this.useCaseSelectedFlag ? false : true,
                      hallucination: true,
                      payload: requestBody
                    }
                    this.covState = {
                      active: this.useCaseSelectedFlag ? false : true,
                      hallucination: true,
                      payload: ragCov
                    }
                    console.log("covState", this.covState)
                  } else {
                    const message = 'File Upload Failed';
                    const action = 'Close';
                    this.hallucinateRetrievalKeplerRes.status = false;
                    this.hallucinateRetrievalKeplerRes.errorMesssage = message;
                    this._snackBar.open(message, action, {
                      duration: 3000,
                      horizontalPosition: 'left',
                      panelClass: ['le-u-bg-black'],
                    });
                  }
                }).catch(error => {
                  this.hallucinateRetrievalKeplerRes.status = false;
                  this.hallucinateRetrievalKeplerRes.errorMesssage = 'File Upload Failed';
                });
                } else {
                  this.hallucinateRetrievalKeplerRes.status = false;
                  this.RagMultiModalResponse.status = true;
                  this.hallucinationResModerationData = res.moderationResults.responseModeration;
                  this.callMultimodalRag().then(res => {
                    console.log(res)
                    if (res != null) {
                      console.log(this.RagMultiModalResponse, "RagMultiModalResponse")                     
                    } else {
                      const message = 'File Upload Failed';
                      const action = 'Close';
                      this.RagMultiModalResponse.status = false;
                      this.RagMultiModalResponse.errorMessage = message;
                      this._snackBar.open(message, action, {
                        duration: 3000,
                        horizontalPosition: 'left',
                        panelClass: ['le-u-bg-black'],
                      });
                    }
                  }).catch(error => {
                    this.RagMultiModalResponse.status = false;
                    this.RagMultiModalResponse.errorMessage = 'File Upload Failed';
                  });

                }




              } else if (this.selectedEmbeddedFileName != '') {
                const requestBody = {
                  fileupload: false,
                  text: prompt,
                  vectorestoreid: this.selectedEmbeddedFileId,
                }
                const ragCov = {
                  fileupload: false,
                  text: prompt,
                  vectorestoreid: this.selectedEmbeddedFileId,
                  complexity: this.selectCoveComplexity
                }
                this.hallucinateRetrievalKepler(requestBody, prompt, tempStringValue, nemoGaurdrail, summaryStatus);
                this.cotState = {
                  active: this.useCaseSelectedFlag ? false : true,
                  hallucination: true,
                  payload: requestBody
                }
                this.thotState = {
                  active: this.useCaseSelectedFlag ? false : true,
                  hallucination: true,
                  payload: requestBody
                }
                this.covState = {
                  active: this.useCaseSelectedFlag ? false : true,
                  hallucination: true,
                  payload: ragCov
                }
                console.log("covState", this.covState)
              } else {
                const message = 'Please select the embeddings';
                const action = 'Close';
                this._snackBar.open(message, action, {
                  duration: 3000,
                  horizontalPosition: 'left',
                  panelClass: ['le-u-bg-black'],
                });
              }
              //   console.log('======Inside rag_Retrieval========== ');
              //   // this.hallRes = [];
              //   // this.bites = [];
              //   // this.sourceBar = [];
            } else {
              this.hallucinateRetrievalKeplerRes.status = false;
              this.hallucinateRetrievalKeplerRes.errorMesssage = 'Coupled Moderation Checks Failed';
              this.RagMultiModalResponse.status = false;
              this.RagMultiModalResponse.errorMessage = 'Coupled Moderation Checks Failed';
            }
          }
          this.templateBasedPayload['status'] = true;
        },
        error => {
          this.hallucinateRetrievalKeplerRes.status = false;
          this.hallucinateRetrievalKeplerRes.errorMesssage = 'Coupled Moderation API Failed';
          this.RagMultiModalResponse.status = false;
          this.RagMultiModalResponse.errorMessage = 'Coupled Moderation API Failed';
          this.spinner = false;
          this.handleError(error, 'Coupled Moderation API Failed')
        }
      );
  }
  callFMConfigApi(configPayload: any, accountName: any, portfolioName: any, tempStringValue: any, prompt: any) {
    accountName = this.selectedAccount;
    portfolioName = this.selectedPortfolio;
    return this.https.post(this.apiEndpoints.fm_config_getAttributes, configPayload).pipe(
      catchError(error => {
        return throwError(error);
      }),
      map((res: any) => {
         
        const response = res.dataList[0];
        if (this.selectedUseCaseName) { // Check if the string has any value
          if (this.selectedUseCaseName === 'Navi') {
            const comp_Payload = this.payloadFMConfig(response, accountName, portfolioName, tempStringValue, prompt);
            return { response, comp_Payload };
          } else {
            const comp_Payload = this.payloadFMConfig_templatebase(response, accountName, portfolioName, tempStringValue, prompt);
            return { response, comp_Payload };
          }
        } else {
          // Handle the case where selectedUseCaseName is empty or null
          const comp_Payload = this.payloadFMConfig(response, accountName, portfolioName, tempStringValue, prompt);
            return { response, comp_Payload };
        }
      })
    );
  }
  callOpenAiApi(prompt: string, tempStringValue: string) {
    this.https
      .post(this.apiEndpoints.fm_api_openAi, { Prompt: prompt, temperature: tempStringValue, model_name: this.selectedLlmModel })
      .subscribe(
        (res: any) => {
          console.log(res.text.length);
          if (res.textlength == 0) {
            this.openAIRes = 'Open Ai failed Reason :' + res.finishReason;
            const message = 'Open Ai failed Reason :' + res.finishReason;
            const action = 'Close';
            this._snackBar.open(message, action, {
              duration: 5000,
              horizontalPosition: 'left',
              panelClass: ['le-u-bg-black'],
            });
          } else {
            console.log(res)
            const boldRegex = /\*\*(.+?)\*\*/;
            const numberedRegex = /\n/g;
            const replacement = "<br>";
            let processedText = res.text.replace(boldRegex, "<b>$1</b>");
            res.text = processedText.replace(numberedRegex, replacement);
            this.openAIRes = res;
            // this.showCompare = true;
            // this.cdr.detectChanges();
          }
        },
        error => {
          this.handleError(error, "OPENAI API FAILED");
        }
      );
  }
  // --------------------------Hallucination API------------------------------
  hallucinateRetrievalKepler(payload: any, prompt: any, tempStringValue: any, nemoGaurdrail: any, summaryStatus: any) {
    const tempSourceebar: any[] = [];
    this.https.post(this.apiEndpoints.rag_Retrieval, payload).subscribe((data: any) => {
      console.log(this.hallucinateRetrievalKeplerRes)
      // this.showSpinner1 = false;
      const res = data.rag_response;
      let sourceBar = []
      let bites = [];
      let ragText = '';
      let page_content = '';
      console.log(res, "HALLUCINATRION RES")
      for (let i = 0; i < res.length; i++) {
        if (res[i]['Faithfulness_Hallucination_score']) {
          this.hallucinateRetrievalKeplerRes.response.hallScore = res[i]['Faithfulness_Hallucination_score'];
        }
        for (let j = 0; j < res[i].length; j++) {
          if (res[i][j].text && res[i][j].text != 'undefined') {
            ragText = ragText + res[i][j].text;
            bites.push({
              text: res[i][j].text,
              source: res[i][j].source,
              baseurl: res[i][j].base64 ? res[i][j].base64 : undefined,
            });
          }

          if (res[i][j].endsrc) {
            for (let k = 0; k < res[i][j].endsrc.length; k++) {
              const temp = {
                source: res[i][j].endsrc[k].source,
                base64: res[i][j].endsrc[k].base64,
              };
              tempSourceebar.push(temp);
            }
          }
          sourceBar = tempSourceebar;
          if (res[i][j].base64 && res[i][j].base64 != 'undefined') {
            this.hallucinateRetrievalKeplerRes.response.base64 = res[i][j].base64;
          }
          if (res[i][j].source && res[i][j].source != 'undefined') {
            this.hallucinateRetrievalKeplerRes.response.source = res[i][j].source;
          }
        }
        if (res[i].page_content && res[i].page_content != 'undefined') {
          page_content = page_content + res[i].page_content;
        }
        if (res[i].openai_score && res[i].openai_score != 'undefined') {
          this.hallucinateRetrievalKeplerRes.response.openAiScore = res[i].openai_score;
        }
        if (res[i]['source-file'] && res[i]['source-file'] != 'undefined') {
          this.hallucinateRetrievalKeplerRes.response.sourceFile = res[i]['source-file'];
        }
      }
      console.log(this.hallucinateRetrievalKeplerRes.response, "RESPOMSE HALLUCINATION")
      this.hallucinateRetrievalKeplerRes.response.text = ragText.replace(/\n/g, '<br>');
      this.hallucinateRetrievalKeplerRes.response.bites = bites;
      if (ragText !== '')
        this.callFMApi(ragText, tempStringValue, nemoGaurdrail, true, undefined, true);
      this.getSummarygEval(ragText, page_content);
    },
      error => {
        console.log(error);
        this.hallucinateRetrievalKeplerRes.status = false;
        this.hallucinateRetrievalKeplerRes.errorMesssage = 'Hallucination API Failed';
      })
  }
  //-------Tranform Text------
  transformText(text: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(text.replace(/\n/g, '<br/>'));
  }
  getSummarygEval(ragText: string, page_content: string) {
    let options = {
      "text": this.prompt,
      "response": ragText,
      "sourcetext": page_content
    };
    // this.https.post("http://100.78.13.150:8000/rai/v1/moderations/gEval",options).subscribe
    this.https.post(this.apiEndpoints.RAG_gEval, options).subscribe(
      (res: any) => {
        this.gEvalres = res;
      },
      error => {
        this.handleError(error)
      }
    );
  }

  callFMTimeApi(hallucinationPostCall: boolean = false) {
    this.https.get(this.apiEndpoints.fm_api_time).subscribe(
      (res: any) => {
        console.log(res);
        if (hallucinationPostCall) {
          console.log("Hallucination Post Call")
          this.fmTimeApiResult.responseModeration = res.requestModeration;
        } else {
          this.fmTimeApiResult = res
        }
      },
      error => {
        this.handleError(error);
      }
    );
  }

  callNemoApi(prompt: any, nemoGaurdrail: any, summaryStatus: any) {
    if (nemoGaurdrail == true) {
      if (summaryStatus == 'PASSED') {
        this.getModerationfornemo(prompt);
      } else {
        // -----------------------------HANDLE FAILED CASE---------------------
        // this.nemoModerationRailRes = 'UNMODERATED';
        // this.nemoModerationRailStatus = 'FAILED';
        // this.nemoModerationRailTime = 'NA';
      }
    }
  }
  getModerationfornemo(prompt: string) {
    const fileData2 = new FormData();
    fileData2.append('text', prompt);
    this.https.post(this.apiEndpoints.nemo_ModerationRail, fileData2).subscribe(
      (res: any) => {
        console.log(res)
        this.nemoModerationRailRes = res
        console.log("NEMO MODERSTION", res)
        // this.nemoModerationRailRes = res.res;
        // this.nemoModerationRailStatus = res.status;
        // this.nemoModerationRailTime = res.time;
      },
      error => {
        this.handleError(error);
      }
    );
  }

  callNemoCheckApi(apiUrl: string, fileData: any, statusProperty: string, timeProperty: string) {
    this.https.post(apiUrl, fileData).subscribe(
      (res: any) => {
        console.log(res)
        this.nemoChecksApiResponses[statusProperty] = res['status'];
        this.nemoChecksApiResponses[timeProperty] = res['time'];
      },
      error => this.handleError(error)
    );
  }

  handleError(error: any, customErrorMessage?: any) {
    console.log(error.status);
    console.log(error.error.detail);
    console.log(error);
    this.spinner = false;
    const message = error.error.details || customErrorMessage || 'API has failed';
    const action = 'Close';
    this.openSnackBar(message, action);
  }
  handleHallucinationSwitch() {
    console.log(this.hallucinationSwitchCheck)
    if (this.hallucinationSwitchCheck) {
      this.getembeddigns()
    }
  }

  // ---------------PAYLOAD--------------------------
  comp_Payload(text: any, temperature: any, LLMinteraction: any, PromptTemplate: any) {
    const payload = {
      AccountName: 'None',
      PortfolioName: 'None',
      // EmojiModeration: this.selectedEmojiVal,
      EmojiModeration: 'yes',
      userid: this.loggedINuserId,
      lotNumber: 1,
      temperature: temperature,
      model_name: this.selectedLlmModel,
      translate: this.selectedTranslate,
      LLMinteraction: LLMinteraction,
      PromptTemplate: PromptTemplate,
      Prompt: text,
      InputModerationChecks: [
        'PromptInjection',
        'JailBreak',
        'Toxicity',
        'Piidetct',
        'Refusal',
        'Profanity',
        'RestrictTopic',
        'TextQuality',
        'CustomizedTheme',
      ],
      OutputModerationChecks: ['Toxicity', 'Piidetct', 'Refusal', 'Profanity', 'RestrictTopic', 'TextQuality', 'TextRelevance'],
      // llm_BasedChecks: ["randomNoiseCheck", "advancedJailbreakCheck"],
      // llm_BasedChecks: this.hallucinationSwitchCheck ? [] : ["randomNoiseCheck", "advancedJailbreakCheck"],
      llm_BasedChecks: this.llmBased,
      ModerationCheckThresholds: {
        PromptinjectionThreshold: 0.7,
        JailbreakThreshold: 0.7,
        PiientitiesConfiguredToBlock: ['IN_AADHAAR', 'IN_PAN', 'US_PASSPORT', 'US_SSN',"AADHAR_NUMBER",
      "PAN_Number"],
        RefusalThreshold: 0.7,
        ToxicityThresholds: {
          ToxicityThreshold: 0.6,
          SevereToxicityThreshold: 0.6,
          ObsceneThreshold: 0.6,
          ThreatThreshold: 0.6,
          InsultThreshold: 0.6,
          IdentityAttackThreshold: 0.6,
          SexualExplicitThreshold: 0.6,
        },
        ProfanityCountThreshold: 1,
        RestrictedtopicDetails: {
          RestrictedtopicThreshold: 0.7,
          Restrictedtopics: ['Terrorism', 'Explosives'],
        },
        CustomTheme: {
          Themename: 'string',
          Themethresold: 0.6,
          ThemeTexts: [''],
        },
        SmoothLlmThreshold: {
          input_pertubation: 0.1,
          number_of_iteration: 4,
          SmoothLlmThreshold: 0.6
        }
      },
    };

    return payload;
  }

  payloadFMConfig(response: any, accountName: any, portfolioName: any, tempStringValue: any, prompt: any) {
    accountName = this.selectedAccount;
    portfolioName = this.selectedPortfolio;
    let payload = {
      AccountName: accountName,
      PortfolioName: portfolioName,
      // EmojiModeration: this.selectedEmojiVal,
      EmojiModeration: 'yes',
      userid: this.loggedINuserId,
      lotNumber: 1,
      temperature: tempStringValue,
      translate: this.selectedTranslate,
      model_name: this.selectedLlmModel,
      LLMinteraction: this.userRoleSettings.llmInteraction,
      // HARD CODE VALUE--------------------------------- NEED TO CHANGE IMPORTANT
      // PromptTemplate: this.selectvalue,
      PromptTemplate: this.selectPromptTemplate,
      Prompt: prompt,
      InputModerationChecks: response.ModerationChecks,
      OutputModerationChecks: response.OutputModerationChecks,
      // llm_BasedChecks: ["randomNoiseCheck", "advancedJailbreakCheck"],
      // llm_BasedChecks: this.hallucinationSwitchCheck ? [] : ["randomNoiseCheck", "advancedJailbreakCheck"],
      llm_BasedChecks: this.llmBased,
      ModerationCheckThresholds: {
        PromptinjectionThreshold: response.ModerationCheckThresholds.PromptinjectionThreshold,
        JailbreakThreshold: response.ModerationCheckThresholds.JailbreakThreshold,
        PiientitiesConfiguredToDetect: response.ModerationCheckThresholds.PiientitiesConfiguredToDetect,
        PiientitiesConfiguredToBlock: response.ModerationCheckThresholds.PiientitiesConfiguredToBlock,
        RefusalThreshold: response.ModerationCheckThresholds.RefusalThreshold,
        ToxicityThresholds: {
          ToxicityThreshold: response.ModerationCheckThresholds.ToxicityThresholds.ToxicityThreshold,
          SevereToxicityThreshold: response.ModerationCheckThresholds.ToxicityThresholds.SevereToxicityThreshold,
          ObsceneThreshold: response.ModerationCheckThresholds.ToxicityThresholds.ObsceneThreshold,
          ThreatThreshold: response.ModerationCheckThresholds.ToxicityThresholds.ThreatThreshold,
          InsultThreshold: response.ModerationCheckThresholds.ToxicityThresholds.InsultThreshold,
          IdentityAttackThreshold: response.ModerationCheckThresholds.ToxicityThresholds.IdentityAttackThreshold,
          SexualExplicitThreshold: response.ModerationCheckThresholds.ToxicityThresholds.SexualExplicitThreshold,
        },
        ProfanityCountThreshold: response.ModerationCheckThresholds.ProfanityCountThreshold,
        RestrictedtopicDetails: {
          RestrictedtopicThreshold: response.ModerationCheckThresholds.RestrictedtopicDetails.RestrictedtopicThreshold,
          Restrictedtopics: response.ModerationCheckThresholds.RestrictedtopicDetails.Restrictedtopics,
        },
        CustomTheme: {
          Themename: response.ModerationCheckThresholds.CustomTheme.Themename,
          Themethresold: response.ModerationCheckThresholds.CustomTheme.Themethresold,
          ThemeTexts: response.ModerationCheckThresholds.CustomTheme.ThemeTexts,
        },
        SmoothLlmThreshold: {
          input_pertubation: 0.1,
          number_of_iteration: 4,
          SmoothLlmThreshold: 0.6
        }
      },
    };


    return payload
  }
  payloadFMConfig_templatebase(response: any, accountName: any, portfolioName: any, tempStringValue: any, prompt: any) {
    accountName = this.selectedAccount;
    portfolioName = this.selectedPortfolio;
    let payload = {
      AccountName: accountName,
      PortfolioName: portfolioName,
      // EmojiModeration: this.selectedEmojiVal,
      EmojiModeration: 'yes',
      userid: this.loggedINuserId,
      lotNumber: 1,
      temperature: tempStringValue,
      translate: this.selectedTranslate,
      model_name: this.selectedLlmModel,
      LLMinteraction: this.userRoleSettings.llmInteraction,
      // HARD CODE VALUE--------------------------------- NEED TO CHANGE IMPORTANT
      // PromptTemplate: this.selectvalue,
      PromptTemplate: this.selectPromptTemplate,
      Prompt: prompt,
      InputModerationChecks: this.requestTemplateGlobal,
      OutputModerationChecks: this.responseTemplateGlobal,
      // llm_BasedChecks: ["randomNoiseCheck", "advancedJailbreakCheck"],
      // llm_BasedChecks: this.hallucinationSwitchCheck ? [] : ["randomNoiseCheck", "advancedJailbreakCheck"],
      llm_BasedChecks: this.llmBased,
      ModerationCheckThresholds: {
        PromptinjectionThreshold: response.ModerationCheckThresholds.PromptinjectionThreshold,
        JailbreakThreshold: response.ModerationCheckThresholds.JailbreakThreshold,
        PiientitiesConfiguredToDetect: response.ModerationCheckThresholds.PiientitiesConfiguredToDetect,
        PiientitiesConfiguredToBlock: response.ModerationCheckThresholds.PiientitiesConfiguredToBlock,
        RefusalThreshold: response.ModerationCheckThresholds.RefusalThreshold,
        ToxicityThresholds: {
          ToxicityThreshold: response.ModerationCheckThresholds.ToxicityThresholds.ToxicityThreshold,
          SevereToxicityThreshold: response.ModerationCheckThresholds.ToxicityThresholds.SevereToxicityThreshold,
          ObsceneThreshold: response.ModerationCheckThresholds.ToxicityThresholds.ObsceneThreshold,
          ThreatThreshold: response.ModerationCheckThresholds.ToxicityThresholds.ThreatThreshold,
          InsultThreshold: response.ModerationCheckThresholds.ToxicityThresholds.InsultThreshold,
          IdentityAttackThreshold: response.ModerationCheckThresholds.ToxicityThresholds.IdentityAttackThreshold,
          SexualExplicitThreshold: response.ModerationCheckThresholds.ToxicityThresholds.SexualExplicitThreshold,
        },
        ProfanityCountThreshold: response.ModerationCheckThresholds.ProfanityCountThreshold,
        RestrictedtopicDetails: {
          RestrictedtopicThreshold: response.ModerationCheckThresholds.RestrictedtopicDetails.RestrictedtopicThreshold,
          Restrictedtopics: response.ModerationCheckThresholds.RestrictedtopicDetails.Restrictedtopics,
        },
        CustomTheme: {
          Themename: response.ModerationCheckThresholds.CustomTheme.Themename,
          Themethresold: response.ModerationCheckThresholds.CustomTheme.Themethresold,
          ThemeTexts: response.ModerationCheckThresholds.CustomTheme.ThemeTexts,
        },
        SmoothLlmThreshold: {
          input_pertubation: 0.1,
          number_of_iteration: 4,
          SmoothLlmThreshold: 0.6
        }
      },
    };


    return payload
  }

  callPrivacyAnalyze(payloadAnalyze: any) {
    let privacyAnalyzeApi = this.apiEndpoints.privacyAnalyzeApi;
    this.https.post(privacyAnalyzeApi, payloadAnalyze).subscribe((priAnzRes) => {
      // this.edited = true;
      console.log(priAnzRes)
      this.privacyResponse.AnazRes = priAnzRes
      this.spinner = false;
      if (this.activeTab == '') {
        this.changeTab('Privacy Result');
      }
    }, error => {
      // You can access status:
      this.handleError(error);
    })
  }
  callPrivacyAnonymize(payloadAnon: any) {
    let privacyAnonApi = this.apiEndpoints.privacyAnonApi;
    this.https.post(privacyAnonApi, payloadAnon).subscribe((priAnonRes: any) => {
      // this.edited = true;
      // IMPORTANT NEED TO HANDLE THIS
      // this.sanitizeResponseData();
      // console.log(this.resData)
      this.privacyResponse.AnonRes = priAnonRes;
      this.spinner = false;
      if (this.activeTab == '') {
        this.changeTab('Privacy Result');
      }
    }, error => {
      // You can access status:
      console.log(error.status);
      this.handleError(error);
    })
  }
  callPrivacyEncrypt(payloadEncrypt: any) {
    // this.apiEndpoints.privacyEncrypt= this.apiEndpoints.privacyEncrypt+'?language='+this.language;
    let privacyEncryptapi = this.apiEndpoints.privacyEncrypt;
    this.https.post(privacyEncryptapi, payloadEncrypt).subscribe((priEncrypt) => {
      // this.edited = true;
      console.log(priEncrypt)
      this.privacyResponse.EncryptRes = priEncrypt
      this.spinner = false;
      this.callPrivacyDecrypt(priEncrypt)
      if (this.activeTab == '') {
        this.changeTab('Privacy Result');
      }
    }, error => {
      // You can access status:
      this.handleError(error);
    })
  }
  callPrivacyDecrypt(payloadDecrypt: any) {
    this.https.post(this.apiEndpoints.privacyDecrypt, payloadDecrypt).subscribe((priDecrypt) => {
      // this.edited = true;
      console.log(priDecrypt)

      this.privacyResponse.decryptedtoggle = false
      this.privacyResponse.DecryptRes = priDecrypt
      this.spinner = false;
      if (this.activeTab == '') {
        this.changeTab('Privacy Result');
      }
    }, error => {
      // You can access status:
      this.handleError(error);
    })
  }
  @ViewChild('p') p!: NgbPopover;
  @ViewChild('pEmoji') pEmoji!: NgbPopover;
  test(p: any) {
    if (this.p.isOpen()) {
      console.log('Popover is open');
      this.p.toggle();
    } else {
      this.p.toggle();
      console.log('Popover is closed');
    }
  }
  openPopOverEmoji() {
    if (this.pEmoji.isOpen()) {
      console.log('Popover is open');
      this.pEmoji.toggle();
    } else {
      this.pEmoji.toggle();
      console.log('Popover is closed');
    }
  }
  selectedEmojiVal: any = 'no';
  selectedNotification!: string;
  tState = false
  tLoading = false

  updateNotificationPreference(f: any, tchoice: any) {

    this.selectedTranslate = tchoice
    if (f.controls['prompt'].value.length != 0) {

      this.tState = false

      if (tchoice == "no") {
        this.tState = false
      } else {
        this.tLoading = true


        // Implement your logic here to handle the change in notification preference
        console.log('Notification Preference updated to:', this.selectedNotification);
        console.log('prompt', f.controls['prompt'].value);
        let payload = {
          "Prompt": f.controls['prompt'].value,
          "choice": tchoice
        }
        this.postTranslateApi(payload)
      }
    } else {
      const message = 'Please enter the prompt';
      const action = 'Close';
      this._snackBar.open(message, action, {
        duration: 3000,
        horizontalPosition: 'left',
        panelClass: ['le-u-bg-black'],
      });
    }
  }
  translatedText!: any;
  postTranslateApi(payload: any) {
    this.https.post(this.apiEndpoints.Moderationlayer_Translate, payload).subscribe((res: any) => {
      console.log(res)
      this.tState = true
      this.tLoading = false
      this.translatedText = res
    }, error => {
      this.tLoading = false
      this.handleError(error)
    })
  }


  // MULTIMODEL

  multiModel: any = false;
  imagePath: any = ''
  selectedFileName: any = ''
  imgShowUrl: any = ''

  privAnonImgUrl2 = '';
  ocrvalue: string = 'Tesseract';
  portfolioName_value = '';
  accountName_value = '';
  exclusionList_value = '';
  privAnzImgUrl2 = '';
  privAnzOutput = '';
  profImageAnalyse = '';
  analyze: any = '';
  fairness_image: any;
  fairness_response: any;
  imagePromptInjection: any;
  imageJailbreak: any;
  imageRestrictedTopic: any;
  imageFailedCases: any = {
    modelBased: [],
    templateBased: []
  };
  demoFileMultimodel: any = [];
  fileMultiModel: any = '';
  selectedFileNameMultiModel: any = '';
  filesMultiModel: any = [];

  resetMultiModelResult() {
    this.analyze = ''
    this.privAnzOutput = ''
    this.imagePromptInjection = '';
    this.imageJailbreak = '';
    this.imageRestrictedTopic = '';
    this.fairness_response = '';
    this.imageFailedCases = {
      modelBased: [],
      templateBased: []
    };
  }

  fileBrowseHandlerMultiModel(file: any) {
    console.log("FILE HANDLER MULTP MODEL")
    this.prepareFilesListMulti(file.target.files);
    this.demoFileMultimodel = this.filesMultiModel;
    this.fileMultiModel = this.filesMultiModel[0];
    const files = file.target.files;
    if (!files[0].type.startsWith('image/')) {
      this.filesMultiModel = [];
      this.demoFileMultimodel = [];
      this.selectedFileNameMultiModel = '';
      this.imagePath = '';
      this.imgShowUrl = '';
      const message = 'Please upload an image file';
      const action = 'Close';
      this._snackBar.open(message, action, {
        duration: 3000,
        horizontalPosition: 'left',
        panelClass: ['le-u-bg-black'],
      });
      return;
    }
    if (files.length > 0) {
      this.selectedFileNameMultiModel = files[0].name;
    }
    const reader = new FileReader();
    this.imagePath = files;
    reader.readAsDataURL(files[0]);
    reader.onload = (_event) => {
      this.imgShowUrl = reader.result;
    }
    this.hallucinationSwitchCheck = false // making file upload as false
  }
  prepareFilesListMulti(files: Array<any>) {
    this.filesMultiModel = [];
    this.demoFile = [];
    for (const item of files) {
      this.filesMultiModel.push(item);
    }
    this.Placeholder = this.tenantarr.includes('Fairness')?"Enter Context":"Enter Prompt";
  }
  removeFileMultimodel() {
    console.log("REMOVE MULTIMODEL FILE")
    this.filesMultiModel = [];
    this.Placeholder = "Enter Prompt";
    // // this.demoFile = [];
    // this.selectedFileNameMultiModel = '';
    // // this.imagePath = '';
    // this.imgShowUrl = '';
    // // this.file = ''
    // this.resetMultiModelResult();
  }
  callMultimodelTemplateAPI() {
    let templateList = ['Prompt Injection', 'Jailbreak', 'Restricted Topic'];
    // the below code is not being used left for multimodel image template
    // let templateList:any = [] 
    // if (this.selectedUseCaseName == '' || this.selectedUseCaseName == 'Navi') {
    //   if (this.filesMultiModel.length > 0) {
    //     templateList =  ['Prompt Injection', 'Jailbreak', 'Toxicity', 'Profanity', 'Restricted Topic']
    //   }}else{
    //     templateList = this.globalMultiModeltemplateList
    //   }
    // 
    this.fmService.updateMultiModal(true, this.llmEvalPayload.userId, templateList, this.prompt, this.filesMultiModel[0]);
    // const formPayload1 = new FormData();
    // formPayload1.append('AccountName', 'None');
    // formPayload1.append('PortfolioName', 'None');
    // formPayload1.append('userid', 'None');
    // formPayload1.append('lotNumber', '1');
    // formPayload1.append('Prompt', this.prompt);
    // formPayload1.append('Image', this.filesMultiModel[0]);
    // formPayload1.append('TemplateName', "Prompt Injection");
    // formPayload1.append('Restrictedtopics', "Terrorism,Explosives");
    // formPayload1.append('model_name', "gpt4O");

    // this.https.post(this.apiEndpoints.multimodal, formPayload1)
    //   .subscribe(response => {
    //     this.imagePromptInjection = response;
    //     if (this.imagePromptInjection?.result == "FAILED") {
    //       this.imageFailedCases.templateBased.push("Image Prompt Injection")
    //     }
    //     console.log("imagePromptInjection", this.imagePromptInjection);
    //   }, error => {
    //     console.log(error)
    //   });

    // const formPayload2 = new FormData();
    // formPayload2.append('AccountName', 'None');
    // formPayload2.append('PortfolioName', 'None');
    // formPayload2.append('userid', 'None');
    // formPayload2.append('lotNumber', '1');
    // formPayload2.append('Prompt', this.prompt);
    // formPayload2.append('Image', this.filesMultiModel[0]);
    // formPayload2.append('TemplateName', "Jailbreak");
    // formPayload2.append('Restrictedtopics', "Terrorism,Explosives");
    // formPayload2.append('model_name', "gpt4O");


    // this.https.post(this.apiEndpoints.multimodal, formPayload2)
    //   .subscribe(response => {
    //     this.imageJailbreak = response;
    //     if (this.imageJailbreak?.result == "FAILED") {
    //       this.imageFailedCases.templateBased.push("Image Jailbreak Check")
    //     }
    //     console.log("imageJailbreak", this.imageJailbreak);
    //   }, error => {
    //     console.log(error)
    //   });


    // const formPayload3 = new FormData();
    // formPayload3.append('AccountName', 'None');
    // formPayload3.append('PortfolioName', 'None');
    // formPayload3.append('userid', 'None');
    // formPayload3.append('lotNumber', '1');
    // formPayload3.append('Prompt', this.prompt);
    // formPayload3.append('Image', this.filesMultiModel[0]);
    // formPayload3.append('TemplateName', "Restricted Topic");
    // formPayload3.append('Restrictedtopics', "Terrorism,Explosives");
    // formPayload3.append('model_name', "gpt4O");


    // this.https.post(this.apiEndpoints.multimodal, formPayload3)
    //   .subscribe(response => {
    //     this.imageRestrictedTopic = response;
    //     if (this.imageRestrictedTopic?.result == "FAILED") {
    //       this.imageFailedCases.templateBased.push("Image Restricted Topic Check")
    //     }
    //     console.log("imageRestrictedTopic", this.imageRestrictedTopic);
    //   }, error => {
    //     console.log(error)
    //   });
  }
  fairnessImage(formPayload: any) {
    for (let [key, value] of formPayload.entries()) {
      console.log(`${key}: ${value}`);
    }
    this.https.post(this.fairness_image, formPayload).subscribe((res: any) => {
      this.fairness_response = res;
      this.fmService.updateMultiModalKeyVal('fairnessRes', res)
      if (this.tenantarr.includes('Fairness')) {
        this.spinner = false;
        if (this.activeTab == '') {
          this.changeTab('Fairness');
        }
        this.fairnessRes = res; //For Fairness Result Tab
      }

      console.log("FAIR::" + this.fairness_response);
      if (this.fairness_response['percentage bias score'] > 80) {
        this.imageFailedCases.modelBased.push('Image Fairness Check')
      }
    }, error => {
      if (this.tenantarr.includes('Fairness')) {
        this.handleError(error, 'Fairness API Failed')
      }
      console.log(error);
    })
  }

  callMultiModel() {
    const fileData = new FormData();
    this.fileMultiModel = this.filesMultiModel[0];
    fileData.append('magnification', 'false');
    fileData.append('rotationFlag', 'false');
    fileData.append('image', this.fileMultiModel);
    fileData.append('portfolio', this.portfolioName_value);
    fileData.append('account', this.accountName_value);
    fileData.append('exclusionList', this.exclusionList_value);
    let h = {
      Accept: 'application/json',
      'Content-Type': 'multipart/form-data',
    };
    let params = new HttpParams();
    params = params.append('ocr', this.ocrvalue);

    this.privacy_Analyze(fileData, h, params); // privacy based multimodel

    this.profanityImageAnalyse(); // model based multimodel

    this.callMultimodelTemplateAPI(); // template based multimodel

    const formPayload = new FormData();
    formPayload.append('prompt', this.prompt);
    formPayload.append('evaluator', "GPT_4o");
    formPayload.append('image', this.filesMultiModel[0]);

    this.fairnessImage(formPayload); // modelbased multimodel

  }

  privacy_Analyze(fileData: any, h: any, params: any) {
    console.log('Privacy - Analyze');
    this.imageService
      .imgApi(this.privAnzImgUrl2 + '?' + params, fileData, h)
      .subscribe({
        next: (data) => {
          let uniquePII: any = new Set()
          let piiEnt = data?.PIIEntities
          for (let i = 0; i < piiEnt.length; i++) {
            if (piiEnt[i].type != 'my') {
              uniquePII.add(piiEnt[i].type)
            }
          }
          console.log('uniquePII===', uniquePII);
          console.log(piiEnt)
          this.privAnzOutput = uniquePII;
          if (piiEnt.length != 0) {
            this.sharedDataService.updateImageBasedModels("Image Privacy Check","",'modelBased')
            // this.imageFailedCases.modelBased.push('Image Privacy Check')
          }
        },
        error: (error) => {
          console.log(error);
        },
      });
  }
  profanityImageAnalyse() {
    const fileData1 = new FormData();
    this.fileMultiModel = this.filesMultiModel[0];
    fileData1.append('image', this.fileMultiModel);
    fileData1.append('portfolio', this.portfolioName_value);
    fileData1.append('account', this.accountName_value);
    this.https.post(this.profImageAnalyse, fileData1).subscribe(
      (data: any) => {
        this.analyze = data.analyze;
        if (
          this.analyze?.hentai > 0.3 ||
          this.analyze?.porn > 0.3 ||
          this.analyze?.sexy > 0.3 ||
          this.analyze?.neutral > 1 ||
          this.analyze?.drawings > 1
        ) {
          // this.imageFailedCases.modelBased.push("Image Safety Check");
          this.sharedDataService.updateImageBasedModels("Image Safety Check","",'modelBased')
        }
        console.log('this.safetydata===', this.analyze);
      },
      (error: any) => {
        console.log(error);
      }
    );
  }
  openDialog(data: any) {
    console.log("DialogData", data);
  
    if (data.startsWith('data:application/pdf;base64,')) {
      this.dialog.open(ImageDialogComponent, {
        data: { pdf: data, flag: true },
        backdropClass: 'custom-backdrop'
      });
    } else if (data.startsWith('data:image/')) {
      this.dialog.open(ImageDialogComponent, {
        data: { image: data, flag: true },
        backdropClass: 'custom-backdrop'
      });
    } else if (data.startsWith('data:text/csv;base64,')) {
      this.dialog.open(ImageDialogComponent, {
        data: { csv: data, flag: true },
        backdropClass: 'custom-backdrop'
      });
    } else if (data.startsWith('data:text/plain;base64,')) {
      this.dialog.open(ImageDialogComponent, {
        data: { plainText: data, flag: true },
        backdropClass: 'custom-backdrop'
      });
    } else if (data.startsWith('data:video/')) {
      this.dialog.open(ImageDialogComponent, {
        data: { video: data, flag: true },
        backdropClass: 'custom-backdrop'
      });
    } else {
    }
  }

  isCollapsed: boolean = false;

  togglePanel(): void {
    this.isCollapsed = !this.isCollapsed;
  }

  getSelectedValues(): void {
    this.selectedPortfolio = localStorage.getItem('selectedPortfolio') ?? '';
    this.selectedAccount = localStorage.getItem('selectedAccount') ?? '';
    console.log('Selected Portfolio:', this.selectedPortfolio);
    console.log('Selected Account:', this.selectedAccount);
}
}

