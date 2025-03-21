/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, ViewEncapsulation } from '@angular/core';
import { ImageService } from './image.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { ImageDialogComponent } from '../image-dialog/image-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { ImageReportChartComponent } from '../image-report-chart/image-report-chart.component';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import * as saveAs from 'file-saver';
import { ImageHashifyRightModalComponent } from './image-hashify-right-modal/image-hashify-right-modal.component';
import { NonceService } from '../nonce.service';

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.css'],
})
export class ImageComponent {
  // FOR SHIMMER EFFECT
  isLoadingUpload = true;
  //////
  form: FormGroup;
  favoriteSeason: any;
  spinner = false;
  ocrvalue: string = 'Tesseract';
  selectValue: string = '';
  selectedModel: string = 'YOLO Model Attack';
  selectedFairnessModel: string = 'GPT_4o';
  responseArr: any[] = [];
  files: any[] = [];
  demoFile: any[] = [];
  selectedFile: File | any;
  file: File | any;
  portfolioName_value = '';
  accountName_value = '';
  exclusionList_value = '';
  privAnonImgUrl2 = '';
  privAnzImgUrl2 = '';
  privVerImgUrl = '';
  privHashImgUrl = '';
  profImageAnalyse = '';
  security_yolo_attack = '';
  security_yolo_defense = '';
  user = 'admin';
  privAnzOutput = '';
  outPrivAnz: any[] = [];
  outputImg: any[] = [];
  imagePath: string = '';
  privAnzRes: any = false;
  imageOutput: any = false;
  imageAnalysePath = '';
  analyze: any = '';
  imgaeBlurred: any;
  imageArray: any[] = [];
  successMessage = '';
  errorMessage = '';
  imgOp = false;
  table = false;
  edited = false;
  imageMode = true;
  dicomMode = false;
  isCollapsed: boolean = true;
  isOpen: boolean = false;
  imgExpl: any
  redactedImg = false
  imageExplainabilityUrl: any;
  fairness_image: any;
  fairness_response: any;
  selectType:any = 'Privacy'
  filePreview: any = '';
  sampleImageSelected= false;

  ocr_options = ['Tesseract', 'EasyOcr', 'ComputerVision'];
  fairness_models = ['GPT_4o'];
  options = [
    {
      viewValue: 'Privacy - Analyze',
      value: 'Privacy - Analyze',
    },
    {
      viewValue: 'Privacy - Anonymize',
      value: 'Privacy - Anonymize',
    },
    {
      viewValue: 'Privacy - Hashify',
      value: 'Privacy - Hashify',
    }
    // {
    //   viewValue: 'Fairness',
    //   value: 'Fairness',
    // },
  ];
  models = [
    {
      "viewValue": "YOLO Model Attack",
      "value": "YOLO Model Attack"
    },
    {
      "viewValue": "YOLO Model Defense",
      "value": "YOLO Model Defense"
    }];
  sampleSrc1 = environment.imagePathurl + '/assets/image/PII_handwritten.jpg';
  sampleSrc2 = environment.imagePathurl + '/assets/image/invoice.png';
  sampleSrc3 = environment.imagePathurl + '/assets/image/Safety_nfsw.png';
  sampleSrc4 = environment.imagePathurl + '/assets/image/Safety_nfsw.png';
  PrivacyAnzUniqueData: any = [];
  privacyHasifyMap: any = [];
  privacy_analyzeFlag: boolean = false;

  constructor(
    private imageService: ImageService,
    public _snackBar: MatSnackBar,
    private https: HttpClient,
    public dialog: MatDialog,
    private fb: FormBuilder,public nonceService:NonceService
  ) {
    this.form = this.fb.group({
      languageModel: ['', Validators.required],
      option: ['', Validators.required],
      securityModel: [''],
      fairnessModel: [''],
      fairnessPrompt: ['']
    });
  }
  ngOnInit(): void {
    console.log('This is unstructured text component');
    let ip_port: any;
    let temuser = 'admin';
    // user call should happen here
    this.user = temuser;
    // geting list of api from  local sotragge
    ip_port = this.getLocalStoreApi();

    // seting up api list
    this.setApilist(ip_port);

    // set timeout for isloading

    this.isLoadingUpload = false;

  }

  handleError(error: any, customErrorMessage?: any) {
    this.spinner = false;
    console.log(error)
    console.log(error.status);
    console.log(error.error.detail);
    let message
    if (error.status === 500) {
      message = "Internal Server Error. Please try again later.";
    } else {
      message = error.error.details || error.error.detail || error.error.message || customErrorMessage || 'API has failed';
    }
    const action = 'Close';
    this.openSnackBar(message, '✖');
  }
  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, '✖', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'top',
      panelClass: ['le-u-bg-black'],
    });
  }

  handleSelectTypeChange(){
    if (this.selectType === 'Privacy'){
      this.options = [
        {
          viewValue: 'Privacy - Analyze',
          value: 'Privacy - Analyze',
        },
        {
          viewValue: 'Privacy - Anonymize',
          value: 'Privacy - Anonymize',
        },
        {
          viewValue: 'Privacy - Verify',
          value: 'Privacy - Verify',
        },
        {
          viewValue: 'Privacy - Hashify',
          value: 'Privacy - Hashify',
        }
      ]
      this.selectValue = ''
    }
    if (this.selectType === 'Safety'){
      console.log("SAFETY")
      // this.options = [
      //   {
      //     viewValue: 'Safety - ImageAnalyse',
      //     value: 'Profanity - ImageAnalyse',
      //   }
      // ]
      this.selectValue = 'Profanity - ImageAnalyse'
    }
    if (this.selectType === 'Explainability'){
      // this.options = [
      //   {
      //     viewValue: 'Image Explainability',
      //     value: 'Helm_Explain - ImageAnalyse',
      //   }
      // ]
      this.selectValue = 'Helm_Explain - ImageAnalyse'
    }
    if (this.selectType === 'Security'){
      // this.options = [
      //   {
      //     viewValue: 'Security',
      //     value: 'Security',
      //   }
      // ]
      this.selectValue = 'Security'
    }
  }

  // used to set the api list urls
  setApilist(ip_port: any) {
    this.privAnonImgUrl2 =
      ip_port.result.Privacy + ip_port.result.Privacy_image_anonymize; // + environment.privAnonImgUrl2
    this.privAnzImgUrl2 =
      ip_port.result.Privacy + ip_port.result.Privacy_image_analyze; //+ environment.privAnzImgUrl2
    this.privVerImgUrl =
      ip_port.result.Privacy + ip_port.result.Privacy_image_verify; //+ environment.privVerImgUrl
    this.privHashImgUrl =
      ip_port.result.Privacy + ip_port.result.Privacy_image_hashify;
    //+ environment.privHashImgUrl
    this.imageExplainabilityUrl = ip_port.result.Image_Explain + ip_port.result.ImageGen_Analyze

    this.profImageAnalyse = ip_port.result.Profanity + ip_port.result.Profan_Image_Analyse;
    this.security_yolo_attack = ip_port.result.YOLODEMO + ip_port.result.YOLODEMO_Attack;
    this.security_yolo_defense = ip_port.result.YOLODEMO + ip_port.result.YOLODEMO_Defense;
    this.fairness_image = ip_port.result.FairnessAzure + ip_port.result.FairnessImage;
  }
  getLocalStoreApi() {
    let ip_port;
    if (localStorage.getItem('res') != null) {
      const x = localStorage.getItem('res');
      if (x != null) {
        return (ip_port = JSON.parse(x));
      }
    }
  }
  openDialog(data: any) {
    this.dialog.open(ImageDialogComponent, {
      data: { image: data, flag: true },
      backdropClass: 'custom-backdrop'
    });
    console.log("dataImage", data)
  }

  onFileChange(event: any) {
    const reader = new FileReader();
    reader.onload = (e: any) => {
      const text = e.target.result;
      console.log(text);
    };
    reader.readAsText(event.target.files[0]);
  }
  ontoglechange(event: any) {
    console.log(event.checked);
    if (event.checked == true) {
      this.imageMode = false;
      this.dicomMode = true;
    } else {
      this.imageMode = true;
      this.dicomMode = false;
    }
  }

  removeFile() {
    this.demoFile = [];
    this.imageArray = [];
    this.imageOutput = false;
    this.files = [];
    this.favoriteSeason = '';
    this.filePreview='';
    this.resetAll();
  }
  submit() {
    this.getSelectedValues();
    this.redactedImg = false
    this.imageOutput = false;
    console.log(this.selectValue)
    if (this.ocrvalue === '' || this.selectValue === '') {
      if (this.ocrvalue === '' && this.selectValue === '') {
        this.openSnackBar('Please select a Language Model and Option before submitting', 'Close');
      } else if (this.ocrvalue === '') {
        this.openSnackBar('Please select a Language Model before submitting', 'Close');
      } else if (this.selectValue === '') {
        this.openSnackBar('Please select an Option before submitting', 'Close');
      }
      return;
    }
    if (this.files.length === 0) {
      this.openSnackBar('Please upload a file before submitting', 'Close');
      return
    }
    this.resetAll();
    this.spinner = true;
    console.log('ocr value', this.ocrvalue);
    const fileData = new FormData();
    const profImagefileData = new FormData();
    this.selectedFile = this.demoFile[0];
    fileData.append('magnification', 'false');
    fileData.append('rotationFlag', 'false');
    fileData.append('image', this.selectedFile);
    if (this.portfolioName_value && this.portfolioName_value.trim() !== '') {
      fileData.append('portfolio', this.portfolioName_value);
    }
    if (this.accountName_value && this.accountName_value.trim() !== '') {
      fileData.append('account', this.accountName_value);
    }
    if (this.exclusionList_value && this.exclusionList_value.trim() !== '') {
      fileData.append('exclusionList', this.exclusionList_value);
      }

    profImagefileData.append('image', this.selectedFile);
    // for fairness
    const formPayload = new FormData();
    formPayload.append('prompt', this.form.value.fairnessPrompt);
    formPayload.append('evaluator', this.form.value.fairnessModel);
    formPayload.append('image', this.selectedFile);

    let h = {
      Accept: 'application/json',
      'Content-Type': 'multipart/form-data',
    };
    let params = new HttpParams();
    params = params.append('ocr', this.ocrvalue);
    if (this.selectValue == 'Privacy - Anonymize') {
      this.privacy_Anonymize(fileData, h, params);
    } else if (this.selectValue == 'Privacy - Hashify') {
      this.privacy_Hashify(fileData, h, params);
    } else if (this.selectValue == 'Privacy - Analyze') {
      this.privacy_Analyze(fileData, h, params);
    } else if (this.selectValue == 'Privacy - Verify') {
      this.privacyVerify(fileData, h, params);
    } else if (this.selectValue == 'Profanity - ImageAnalyse') {
      this.profanityImageAnalyse();
    } else if (this.selectValue == 'Security') {
      this.security();
    } else if (this.selectValue == 'Helm_Explain - ImageAnalyse') {
      this.imageExplainability();
    } else if (this.selectValue == 'Fairness') {
      this.fairness(formPayload);
    }else{
      this.spinner = false;
      this.openSnackBar('Please select an option before submitting', 'Close');
    }
  }

  privacy_Anonymize(fileData: any, h: any, params: any) {
    console.log('Privacy - Anonymize function call');
    this.privAnzOutput = '';
    this.outPrivAnz = [];
    this.outputImg = [];
    this.imageOutput = false;
    this.imageService
      .imgApi(this.privAnonImgUrl2 + '?' + params, fileData, h)
      .subscribe({
        next: (data) => {
          this.imagePath = data;
          this.outputImg.push(this.imagePath);
          console.log('this.data===', data);
          this.spinner = false;
          this.imgOp = true;
          this.table = true;
        },
        error: (error) => {
          // You can access status:
          console.log(error.status);
          this.spinner = false;
          this.edited = false;
          this.successMessage = '';
          this.errorMessage = error.error.message;
          // console.log(error.error.detail)
          this.handleError(error)
        },
      });

    this.selectedFile = '';
  }

  privacy_Hashify(fileData: any, h: any, params: any) {
    console.log('Privacy - Hashify');
    this.privAnzOutput = '';
    this.outPrivAnz = [];
    this.outputImg = [];
    this.imageOutput = false;
    this.imageService
      .imgApi(this.privHashImgUrl + '?' + params, fileData, h)
      .subscribe({
        next: (data) => {
          this.imagePath = data.img;
          this.outputImg.push(this.imagePath);
          this.spinner = false;
          this.imgOp = true;
          this.table = true;
          this.privacyHasifyMap = data.map;
          // this.privAnzOutput = data;
          // this.outPrivAnz.push(data.map);
          // this.privAnzRes = true;
        },
        error: (error) => {
          // You can access status:
          console.log(error.status);
          this.spinner = false;
          this.edited = false;
          this.successMessage = '';
          this.errorMessage = error.error.message;
          // console.log(error.error.detail)
          this.handleError(error)
        },
      });

    this.selectedFile = '';
  }
  privacy_Analyze(fileData: any, h: any, params: any) {
    console.log('Privacy - Analyze');
    this.imagePath = '';
    this.outputImg = [];
    this.outPrivAnz = [];
    this.imageOutput = false;
    this.imageService
      .imgApi(this.privAnzImgUrl2 + '?' + params, fileData, h)
      .subscribe({
        next: (data) => {
          // this.privAnzOutput = data;
          const typesSet = new Set(data.PIIEntities.map((entity: { type: any; }) => entity.type));
          const uniqueTypes = Array.from(typesSet);
          this.PrivacyAnzUniqueData = uniqueTypes;
          this.privacy_analyzeFlag = true;
          // this.outPrivAnz.push(data);
          // this.imgOp = true;
          this.spinner = false;
          this.privAnzRes = true;
        },
        error: (error) => {
          // You can access status:
          console.log(error.status);
          this.spinner = false;
          this.edited = false;
          this.successMessage = '';
          this.errorMessage = error.error.message;
          // console.log(error.error.detail)
          this.handleError(error)
        },
      });
  }
  privacyVerify(fileData: any, h: any, params: any) {
    console.log('Privacy - Verify');
    this.imagePath = '';
    this.outputImg = [];
    this.outPrivAnz = [];
    this.imageOutput = false;
    this.imageService
      .imgApi(this.privVerImgUrl + '?' + params, fileData, h)
      .subscribe({
        next: (data) => {
          this.imagePath = data;
          this.outputImg.push(data);
          // this.outputImage=(atob(data));
          // console.log(this.outputImage);
          this.spinner = false;
          this.imgOp = true;
          this.table = true;
        },
        error: (error) => {
          // You can access status:
          console.log(error.status);
          this.spinner = false;
          this.edited = false;
          this.successMessage = '';
          this.errorMessage = error.error.message;
          // console.log(error.error.detail)
          this.handleError(error)
        },
      });
  }
  profanityImageAnalyse() {
    // this.imgOp = false;
    this.imageOutput = false;
    this.outputImg = [];
    this.privAnzRes = false;
    const fileData1 = new FormData();
    this.selectedFile = this.demoFile[0];
    fileData1.append('image', this.selectedFile);
    if (this.portfolioName_value && this.portfolioName_value.trim() !== '') {
      fileData1.append('portfolio', this.portfolioName_value);
    }
    if (this.accountName_value && this.accountName_value.trim() !== '') {
      fileData1.append('account', this.accountName_value);
    }
    this.https.post(this.profImageAnalyse, fileData1).subscribe(
      (data: any) => {
        console.log(data);
        this.imageOutput = true;
        this.imageAnalysePath = data.ORIGINAL;
        this.analyze = data.analyze;
        this.imgaeBlurred = data.BLURRED;
        this.imageArray.push(data.img);
        // this.outputImg.push(this.imagePath)
        this.imgOp = true;
        // this.outputImage=(atob(data));
        console.log('this.data===', data);
        this.spinner = false;

        // this.table = true;
      },
      (error: any) => {
        // You can access status:
        this.spinner = false;
        this.edited = false;
        this.successMessage = '';
        this.errorMessage = error.error.message;
        this.handleError(error)
      }
    );
  }
  imageExplainability() {
    const fileData1 = new FormData();
    this.selectedFile = this.demoFile[0];
    fileData1.append('image', this.selectedFile);
    this.https.post(this.imageExplainabilityUrl, fileData1).subscribe((data: any) => {
      // this.imageOutput = true
      // this.imageOutput = false;
      this.imagePath = data.img;
      // this.imagePath = data;
      this.outputImg.push(this.imagePath);
      console.log('this.data===', data);
      this.spinner = false;
      this.imgOp = true;
      this.table = true;
      this.analyze = data
      this.imgExpl = data
      this.redactedImg = true
      console.log("image explainability", data.img)
      this.imageAnalysePath = data.img;
      this.spinner = false;
      // this.showSpinner = false;
    }, error => {
      if (error.status == 430) {
        this.spinner = false;
        console.log(error.error.detail)
        console.log(error)
        const message = error.error.detail
        const action = "Close"
        this._snackBar.open(message, '✖', {
          duration: 3000,
          horizontalPosition: 'left',
          panelClass: ['le-u-bg-black'],
        });
      } else {
        this.spinner = false;
        console.log(error.error.detail)
        console.log(error)
        const message = "The Api has failed"
        const action = "Close"
        this._snackBar.open(message, '✖', {
          duration: 3000,
          horizontalPosition: 'left',
          panelClass: ['le-u-bg-black'],
        });
      }
    })

  }
  security() {
    // output is zip file
    if (this.selectedModel == 'YOLO Model Attack') {
      const attackForm = new FormData();
      for (let i = 0; i < this.demoFile.length; i++) {
        this.selectedFile = this.demoFile[i];
        attackForm.append('DataFile', this.selectedFile);
      }
      this.https.post(this.security_yolo_attack, attackForm, { responseType: 'blob' }).subscribe((resp: Blob) => {
        const filename = this.genFile();
        saveAs(resp, filename);
        const message = 'Your file has been downloaded. Please check your downloads folder.';
        const action = 'Close';
        this._snackBar.open(message, '✖', {
          duration: 3000,
          horizontalPosition: 'left',
          panelClass: ['le-u-bg-black'],
        });
        this.spinner = false;
      }, error => {
        this.handleError(error)
      })

    } else if (this.selectedModel == 'YOLO Model Defense') {
      const defenseForm = new FormData();
      for (let i = 0; i < this.demoFile.length; i++) {
        this.selectedFile = this.demoFile[i];
        defenseForm.append('DataFile', this.selectedFile);
      }
      this.https.post(this.security_yolo_defense, defenseForm, { responseType: 'blob' }).subscribe((resp: any) => {
        const filename = this.genFile();
        saveAs(resp, filename);
        this.spinner = false;
      }, error => {
        this.spinner = false;
        this.handleError(error)
      })

    }
  }
  fairness(formPayload: any) {
    console.log(formPayload)
    if (formPayload.get('prompt') == null || formPayload.get('prompt') == '') {
      this.spinner = false;
      this.openSnackBar('Please enter a prompt before submitting', 'Close',);
      return;
    }
    this.https.post(this.fairness_image, formPayload).subscribe((res: any) => {
      this.fairness_response = res;
      this.imgOp = true;
      this.spinner = false;
    }, error => {
      this.spinner = false;
      this.handleError(error)
    })
    console.log("FAIR::" + this.fairness_response);
  }
  genFile(): string {
    const timestamp = new Date().getTime();
    return `file_${timestamp}`;
  }

  toggleCollapse() {
    this.isCollapsed = !this.isCollapsed;
    // this.cdr.detectChanges();
  }


  toggleCaret() {
    this.isOpen = !this.isOpen;
  }
  openExplRightSideModal() {
    const dialogRef = this.dialog.open(ImageReportChartComponent, {
      width: '52vw',
      height: 'calc(100vh - 57px)', // Subtract the height of the navbar
      position: {
        top: '57px', // Position the modal below the navbar
        right: '0'
      },
      backdropClass: 'custom-backdrop',
      data: {
        analyze: this.imgExpl,
        tenent: "Explainability",
        type: "upload"
      }
    });

    dialogRef.afterClosed().subscribe(() => {
    });
  }
  openHashifySideModal() {
    const dialogRef = this.dialog.open(ImageHashifyRightModalComponent, {
      width: '52vw',
      height: 'calc(100vh - 57px)',
      position: {
        top: '57px',
        right: '0'
      },
      backdropClass: 'custom-backdrop',
      data: { data: this.privacyHasifyMap }
    });
  }

  //
  selectOptionOcr(e: any) {
    console.log('Selected option ID:', e.value);
    this.ocrvalue = e.value;
  }
  selectOption(e: any) {
    console.log('Selected option ID:', e.value);
    this.selectValue = e.value;
  }
  selectSecurityModel(e: any) {
    this.selectedModel = e.value;
  }
  selectFairnessModel(e: any) {
    this.selectedFairnessModel = e.value;
  }

  //

  fileBrowseHandler(imgFile: any) {
    this.favoriteSeason = '';
    // this.browseFilesLenth = imgFile.target.files.length;
    console.log(imgFile.target.files);
    this.prepareFilesList(imgFile.target.files);
    this.demoFile = this.files;
    this.file = this.files[0];
    console.log("Files[0]",this.files[0] )
    // to validate file SAST
    const allowedTypes = ['image/png', 'image/jfif', 'image/jpg','image/jpeg'];
    for(let i =0; i< this.files.length; i++){
      if (!allowedTypes.includes(this.files[i].type)) {
        this.openSnackBar('Please upload a valid image file', 'Close');
        this.files = [];
        this.demoFile = [];
        this.file = '';
        this.filePreview = '';
        return ;
      }
    }
    const reader = new FileReader();
    reader.readAsDataURL(this.files[0]);
    reader.onload = (_event) => {
      const base64String = reader.result as string;
      this.filePreview = base64String;
      console.log("filePreview",this.filePreview )
    };
    // this.uploadDocument(this.file);
    //  console.log("on choosing")
  }

  prepareFilesList(files: Array<any>) {
    this.files = [];
    this.demoFile = [];
    for (const item of files) {
      const cleanedName = item.name.replace(/\[object Object\]/g, '');
      const newFile = new File([item], cleanedName, { type: item.type });
      this.files.push(newFile);
    }
    this.uploadFilesSimulator(0, files);
  }

  uploadFilesSimulator(index: number, files: any) {
    setTimeout(() => {
      if (index === this.files.length) {
        console.log('RETURN');
        return;
      } else {
        this.files[index].progress = 0;
        const progressInterval = setInterval(() => {
          if (this.files[index].progress >= 100) {
            clearInterval(progressInterval);
          } else {
            console.log('ELSE BLOCK');
            this.files[index].progress += 10;
          }
        }, 200);
      }
    }, 1000);
  }
  viewchange() {
    console.log('view change', this.favoriteSeason);
  }

  onClick(s: any) {
    console.log('Clicked image URL:', s);
    this.sampleImageSelected = true;
    fetch(s)
      .then((response) => response.blob())
      .then((blob) => {
        const file = new File(
          [blob],
          s.replace(/^.*[\\\/]/, { type: 'image/png' })
        );
        const abc: any = [];
        abc.push(file);
        // this.imgBrowseHandler(file)
        // console.log("conver6ec file ", file);
        this.selectedFile = file;
        // this.files.push(file)
        this.prepareFilesList(abc);

        this.demoFile.push(file);

        // this.demoFilesLenght = this.demoFile.length
        // this.cdr.detectChanges();
        const reader = new FileReader();
        reader.onloadend = () => {
          const base64data = reader.result as string;
          this.filePreview = base64data;
          console.log("filePreview",this.filePreview )
        };
        reader.readAsDataURL(blob);
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
  openRightSideModal() {
    const dialogRef = this.dialog.open(ImageReportChartComponent, {
      width: '52vw',
      height: 'calc(100vh - 57px)', // Subtract the height of the navbar
      position: {
        top: '57px', // Position the modal below the navbar
        right: '0',
      },
      backdropClass: 'custom-backdrop',
      data: {
        analyze: this.analyze,
        tenent: 'Safety',
      },
    });

    dialogRef.afterClosed().subscribe(() => { });
  }
  resetAll() {
    this.filePreview='';
    this.imgOp = false;
    this.imageOutput = false;
    this.privAnzRes = false;
    this.privacy_analyzeFlag = false;
    this.fairness_response = '';
    this.PrivacyAnzUniqueData = [];
    this.privacyHasifyMap = [];
    this.outputImg = []
  }

  getSelectedValues(): void {
    this.portfolioName_value = localStorage.getItem('selectedPortfolio') ?? '';
    this.accountName_value = localStorage.getItem('selectedAccount') ?? '';
    console.log('Selected Portfolio:', this.portfolioName_value);
    console.log('Selected Account:', this.accountName_value);
  }
}
