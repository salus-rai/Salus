/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient } from '@angular/common/http';
import { Component, ViewEncapsulation, OnInit, ViewChild, ElementRef, TemplateRef} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { PagingConfig } from '../_models/paging-config.model';
import { saveAs } from 'file-saver';
import { FormControl, AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-video',
  templateUrl: './video.component.html',
  styleUrls: ['./video.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class VideoComponent implements OnInit{
  @ViewChild('videoDialog') videoDialog!: TemplateRef<any>;
  @ViewChild('fileInput') fileInput!: ElementRef;
  // FOR SHIMMER EFFECT
  isLoadingUpload = true;
  isLoadingTable = true;
  /////
  form1: FormControl;
  form2: FormControl;
  videoUrl: SafeResourceUrl | null = null;
  showSpinner1 = false;
  selectValue: string = '';
  showFileInput = false;
  selectedOptions: string[] = [];
  
  constructor(public _snackBar: MatSnackBar, private https: HttpClient, private dialog: MatDialog, private sanitizer: DomSanitizer) {
    this.form1 = new FormControl(null, this.fileSelectedValidator);
    this.form2 = new FormControl(null, this.optionSelectedValidator.bind(this));

    this.pagingConfig = {
      itemsPerPage: this.itemsPerPage,
      currentPage: this.currentPage,
      totalItems: this.totalItems
    }
  }
  fileSelectedValidator(control: AbstractControl): ValidationErrors | null {
    if (control.value == null || control.value.length === 0) {
      return { 'noFileSelected': true };
    }
    return null;
  }
  optionSelectedValidator(control: AbstractControl): ValidationErrors | null {
    if (this.selectedOptions.length === 0) {
      return { 'noOptionSelected': true };
    }
    return null;
  }

  openDialog(videoUrl: string): void{
    console.log("Opening dialog with URL: ", videoUrl);

    const sanitizedUrl = this.sanitizer.bypassSecurityTrustResourceUrl(videoUrl);

    console.log("Sanitized URL: ", sanitizedUrl);

    const dialogRef=  this.dialog.open(this.videoDialog, {
        data: { safeUrl: sanitizedUrl },
        position: { right : '0px', bottom: '0px' },
        width: '55%',
        height: '90%'
      });
      dialogRef.afterOpened().subscribe(()=>{console.log("Dialog data after opened:", dialogRef.componentInstance?.data);});
  }

  currentPage: number = 1;
  itemsPerPage: number = 5;
  totalItems: number = 0;

  files: any[] = [];
  demoFile: any[] = [];
  selectedFile: File | any;
  file: File | any;
  selectedSubCategory: string = '';

  pagingConfig: PagingConfig = {} as PagingConfig;

  options = [
    { value: 'NudityMasking', viewValue: 'Nudity Masking' },
    { value: 'SafetyMasking', viewValue: 'Safety Masking' },
    // { value: 'FaceAnonymize', viewValue: 'Face Anonymize' },
    { value: 'PIIAnonymize', viewValue: 'PII Anonymize' },
    // { value: 'CustomMask', viewValue: 'Custom Mask' }
  ];

  ngOnChanges(): void {
    this.showFileInput = this.selectedOptions.includes('CustomMask');
  }


  userId = ""

  processing = ""
  result: any
  refreshTable = false


  getFile = ""
  uploadFile = ""
  DocProcessing_getFileContent = ""
  onFileChange(event: any) {
    const reader = new FileReader();
    reader.onload = (e: any) => {
      const text = e.target.result;
      console.log(text);
    };
    reader.readAsText(event.target.files[0]);
  }
  ngOnInit(): void {
    let ip_port: any

    let user = this.getLogedInUser()

    ip_port = this.getLocalStoreApi()
    this.setApilist(ip_port)
    this.isLoadingUpload = false;
    this.getVideoFilesList()


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
  setApilist(ip_port: any) {
    this.getFile = ip_port.result.DocProcess + ip_port.result.DocProcess_getFiles  // + environment.getFile

    this.uploadFile = ip_port.result.DocProcess + ip_port.result.DocProcess_uploadFile   //+ environment.uploadFile 

    this.DocProcessing_getFileContent = ip_port.result.DocProcess + ip_port.result.DocProcessing_getFileContent   //+ environment.uploadFile

  }

  getVideoFilesList() {
    this.https.get(this.getFile + "/" + this.userId + "/video").subscribe
      ((res: any) => {

        this.result = res
        this.pagingConfig.totalItems = this.result.length;
        console.log("this.result====", this.result)

        this.refreshTable = true
        this.isLoadingTable = false;
      }, error => {
        console.log(error.status);
        console.log(error)
        const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
        this.processing = "Failed"
        const action = "Close"
        this._snackBar.open(message, action, {
          duration: 3000,
          horizontalPosition: 'left',
          panelClass: ['le-u-bg-black'],
        });


      })
  }
  onTableDataChange(event: any) {
    this.pagingConfig.currentPage = event;
    this.pagingConfig.totalItems = this.result.length;
  }
  onTableSizeChange(event: any): void {
    this.pagingConfig.itemsPerPage = event.result.value;
    this.pagingConfig.currentPage = 1;
    this.pagingConfig.totalItems = this.result.length;
  }

  isCompleted(data: any): boolean {
    if (data == "Completed") {
      return true
    }
    else {
      return false
    }

  }
  submit() {
    this.form2.updateValueAndValidity();
    const message = this.form1.invalid && this.form2.invalid ? 'Please select a Video File & Category before Submitting' :
                    this.form1.valid && this.form2.invalid ? 'Please select a Category before Submitting' :
                    this.form1.invalid && this.form2.valid ? 'Please select a Video File before Submitting' : '';

    if (message) {
    this._snackBar.open(message, '✖', {
    horizontalPosition: 'center',
    verticalPosition: 'top',
    duration: 3000,
    });
    return;
    }
    console.log("submit")
    this.upload_file()
  }
  upload_file() {
    this.showSpinner1 = true;
    let userId = this.getLogedInUser()
    const fileData = new FormData();
    this.selectedFile = this.demoFile[0];
    console.log("demofile", this.demoFile)
    if (['video/mp4', 'video/webm', 'video/ogg'].includes(this.selectedFile.type)) {
      console.log("inside if video file")
      fileData.append('file', this.selectedFile);
      fileData.append('userId', userId)
      fileData.append('categories', "video")
      fileData.append('subCategoey', this.selectedOptions.join(','));
      this.uploadFileApiCall(fileData)
    } else {
      this.files = []
      this.demoFile= []
      const message = "Please Select Correct Video File Format"
      // this.processing = "Failed"
      const action = "Close"
      this._snackBar.open(message, action, {
        duration: 3000,
        horizontalPosition: 'left',
        panelClass: ['le-u-bg-black'],
      });
    }
  }
  uploadFileApiCall(fileData: any) {
    this.https.post(this.uploadFile, fileData).subscribe((res: any) => {
      this.result = res
      this.processing = "Complete"
      console.log("res======", res)
      this.getVideoFilesList()
      this.showSpinner1 = false;
    }, error => {
      // You can access status:
      console.log(error.status);
        // this.showSpinner1 = false;
        console.log(error)
        const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
        this.processing = "Failed"
        const action = "Close"
        this._snackBar.open(message, action, {
          duration: 3000,
          horizontalPosition: 'left',
          panelClass: ['le-u-bg-black'],
        });
        this.showSpinner1 = false;

    })
  }
  // getfileContent(id:any){
  //   this.https.post(this.DocProcessing_getFileContent+id,null).subscribe
  //       ((res: any) => {
  //         // this.showSpinner1=false
  //         console.log("video file name ",res[0].data)
  //         console.log("video file name ",res[0].fileName)
  //         const datax = atob(res[0].data);
  //         console.log("video file name ",datax)
  //         const filename = res[0].fileName;
  //         const byteNumbers= new Array(datax.length);
  //         for (let i = 0; i < datax.length; i++) {
  //           byteNumbers[i] = datax.charCodeAt(i);
  //         }
  //         const byteArray = new Uint8Array(byteNumbers);
  //         const blob = new Blob([byteArray], { type: 'video/mp4' });
  //         saveAs(blob, filename);
  //       }, error => {
  //         // You can access status:
  //         console.log(error.status);
  //         // this.showSpinner1 = false;
  //         // this.edited = false;
  //         console.log(error.error.detail)
  //         console.log(error)
  //         const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
  //         const action = "Close"
  //         this._snackBar.open(message, action, {
  //           duration: 3000,
  //           panelClass: ['le-u-bg-black'],
  //         });
  //       })

  //     }
  getfileContent(documentLink: string){
    console.log('Navigating to:', documentLink);
    window.location.href = documentLink; 
  }

  fileBrowseHandler(imgFile: any) {
    // this.browseFilesLenth = imgFile.target.files.length;
    this.files = [];
    this.demoFile = [];
    this.prepareFilesList(imgFile.target.files);
    this.demoFile = this.files;
    this.file = this.files[0];
        // to validate file SAST
        const allowedTypes = ['video/mp4'];
        for(let i =0; i< this.file.length; i++){
          if (!allowedTypes.includes(this.file[i].type)) {
            this._snackBar.open('Please upload valid file', 'Close', {
              duration: 2000,
            });
            this.file = [];
            return ;
          }
        }
    this.form1.setValue(this.files);
    // this.uploadDocument(this.file);
    //  console.log("on choosing")
  }

  prepareFilesList(files: Array<any>) {
    for (const item of files) {
      // item.progress = 0;
      this.files.push(item);
    }
    this.uploadFilesSimulator(0, this.files);
  }
  uploadFilesSimulator(index: number,files:any) {
    setTimeout(() => {
      console.log(this.files[0].name)
      if (index === this.files.length) {
        return;
      } else {
        this.files[index].progress = 0;
        const progressInterval = setInterval(() => {
          if (this.files[index].progress >= 100) {
            clearInterval(progressInterval);
          } else {
            this.files[index].progress += 10;
          }
        }, 200);
      }
    }, 1000);
  }
  deleteFile(){
    this.files = [];
    this.demoFile = [];
    this.file = null;
  }
  toggleAllSelection(event: any) {
    this.selectedOptions = event.checked ? this.options.map(x => x.value) : [];
    this.form2.updateValueAndValidity();
  }

  reset(){
    this.files = [];
    this.demoFile = [];
    this.file = null;
    this.selectedOptions = [];        
    this.fileInput.nativeElement.value = '';
  }
}
