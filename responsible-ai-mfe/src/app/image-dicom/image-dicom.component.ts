/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, ElementRef, ViewChild } from '@angular/core';
import { DICOMViewerComponent } from '../dicom-lib/dicom-viewer.component';
import * as cornerstoneWADOImageLoader from "cornerstone-wado-image-loader";
import * as cornerstone from "cornerstone-core";
import * as dicomParser from 'dicom-parser';
import { environment } from 'src/environments/environment';
import { ImageDicomService } from './image-dicom.service';
import { Subscription } from 'rxjs';
import { ImageDialogComponent } from '../image-dialog/image-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { FormControl, AbstractControl, ValidationErrors, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';


@Component({
  selector: 'app-image-dicom',
  templateUrl: './image-dicom.component.html',
  styleUrls: ['./image-dicom.component.css']
})
export class ImageDicomComponent {
  // FOR SHIMMER EFFECT
  isLoadingUpload = true;

  //////
  selectedImage: string = '';
  form: FormControl;
  // @ViewChild("fileDropRef", { static: false }) fileDropEl: any = ElementRef;
  @ViewChild(DICOMViewerComponent, { static: true }) viewPort: any = DICOMViewerComponent;

  dicom1 = environment.dicomPathUrl + '/assets/dicom/0_ORIGINAL.dcm'
  dicom2 = environment.dicomPathUrl + '/assets/dicom/1_ORIGINAL.dcm'
  dicom3 = environment.dicomPathUrl + '/assets/dicom/3_ORIGINAL.dcm'

  dicomThumb1 = environment.imagePathurl + '/assets/image/dicomThumb1.png'
  dicomThumb2 = environment.imagePathurl + '/assets/image/dicomThumb2.png'
  dicomThumb3 = environment.imagePathurl + '/assets/image/dicomThumb3.png'


  dicomFile: any[] = [];
  selectedDicomFile: File | any;
  arr: any[] = [];
  preview = false;

  files: any[] = [];
  demoFile: any[] = [];
  selectedFile: File | any;
  file: File | any;

  fileName: string = "TEST";
  progress: number = 0;
  uploadSubscription!: Subscription;

  dicomUrl = environment.dicomUrl
  public ip_port: any
  res1!: SafeUrl;
  res2!: SafeUrl;
  table: boolean = false;
  dicom: boolean = false;
  spinner = false;

  constructor(private _snackBar: MatSnackBar, private dicomService: ImageDicomService, public dialog: MatDialog, public snackBar: MatSnackBar,private sanitizer: DomSanitizer) {

    this.form = new FormControl(null, this.fileSelectedValidator.bind(this));
  }
  fileSelectedValidator(control: AbstractControl): ValidationErrors | null {
    if ((control.value == null || control.value.length === 0) && !this.selectedImage) {
      return { 'noFileSelected': true };
    }
    return null;
  }

  ngOnInit(): void {
    console.log(this.dicomThumb1)
    const promise1 = new Promise((resolve, reject) => {
      this.onclick(this.dicom1);
      resolve("0_ORIGINAL.dcm ");
    });

    const promise2 = new Promise((resolve, reject) => {
      setTimeout(() => {
        this.onclick(this.dicom2);
        resolve("1_ORIGINAL.dcm");
      }, 1000);

    });

    const promise3 = new Promise((resolve, reject) => {
      setTimeout(() => {
        this.onclick(this.dicom3);
        resolve("3_ORIGINAL.dcm");
      }, 2000);
    });



    Promise.all([promise1, promise2, promise3])
      .then((result) => console.log(result));
    cornerstoneWADOImageLoader.external.cornerstone = cornerstone; // inicializa WADO Image loader
    cornerstoneWADOImageLoader.external.dicomParser = dicomParser;
    // configura codecs e web workers
    cornerstoneWADOImageLoader.webWorkerManager.initialize({
      webWorkerPath: './assets/cornerstone/webworkers/cornerstoneWADOImageLoaderWebWorker.js',
      taskConfiguration: {
        'decodeTask': {
          codecsPath: '../codecs/cornerstoneWADOImageLoaderCodecs.js'
        }
      }
    });
    if (localStorage.getItem("res") != null) {
      const x = localStorage.getItem("res")
      if (x != null) {
        this.ip_port = JSON.parse(x)
        console.log("inside parse", this.ip_port.result)
      }
      console.log("ip_port arr v", this.ip_port.result.DICOM)
      console.log("ip_port", this.ip_port)
    }
    this.dicomUrl = this.ip_port.result.DICOM + this.ip_port.result.Privacy_dicom_anonymize //+ environment.dicomUrl

    this.isLoadingUpload = false;
  }

  handleError(error: any, customErrorMessage?: any) {
    console.log(error)
    console.log(error.status);
    console.log(error.error.detail);
    let message
    if (error.status === 500) {
      message = "Internal Server Error. Please try again later.";
    } else {
      message = error.error.detail || error.error.message || "API has failed";
    }
    const action = 'Close';
    this.openSnackBar(message, action);
  }
  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 3000,
      panelClass: ['le-u-bg-black'],
    });
  }
  // -------------HANDEL DICOM IMAGE VIEWER----------------
  loadDICOMImages(files: any, x: any, y: any) {
    console.log("LOAD DICOM IMAGE FUN")
    this.dicom = true;
    this.preview = true;
    if (y == 1) {
      files = this.dicomFile[0];
    } else if (y == 2) {
      files = this.dicomFile[1];
    } else if (y == 3) {
      files = this.dicomFile[2];
    }
    if (files) {
      // console.log("Insdoe if")
      let imageList: any[] = [];
      // const fileList:Array<File> = Array.from(files);
      const fileList: Array<File> = [];
      fileList.push(files)
      // console.log("filelist===",fileList)
      fileList.sort((a, b) => {
        if (a.name > b.name) return 1;
        if (b.name > a.name) return -1;
        return 0;
      })
      //cornerstoneWADOImageLoader.wadouri.fileManager.purge();
      cornerstoneWADOImageLoader.wadouri.dataSetCacheManager.purge();

      // loop thru the File list and build a list of wadouri imageIds (dicomfile:)
      for (let i = 0; i < fileList.length; i++) {
        const dicomFile: File = fileList[i];
        // console.log("dicom==381===",dicomFile)
        const imageId = cornerstoneWADOImageLoader.wadouri.fileManager.add(dicomFile);
        imageList.push(imageId);


      }
      this.viewPort.resetAllTools();
      // now load all Images, using their wadouri
      this.viewPort.loadStudyImages(imageList);
    }
  }

  onclick(s: any) {
    console.log("dicom1===", s)
    fetch(s)
      .then(response => response.blob())
      .then(blob => {
        const file = new File([blob], s.replace(/^.*[\\\/]/, { type: 'dicom/dcm' }))
        console.log("conver6ec file ", file);
        this.selectedDicomFile = file;
        this.dicomFile.push(file)
        this.arr.push(this.dicomFile)
      })
      .catch(error => {
      })
  }

  onClick(s: any) {
    this.selectedImage = s;
    this.form.updateValueAndValidity();
    this.demoFile = []
    this.files = []
    this.preview = false;
    fetch(s)
      .then(response => response.blob())
      .then(blob => {
        // const file = new File([blob], s.replace(/^.*[\\\/]/, { type: 'dicom/dcm' }))
        const cleanedFileName = s.replace(/^.*[\\\/]/, '').replace(/\[object Object\]/g, '');
        const file = new File([blob], cleanedFileName, { type: 'dicom/dcm' });
        this.selectedFile = file;
        this.demoFile.push(file)
        this.files.push(file)
        this.uploadFilesSimulator(0, this.files);
      })
      .catch(error => {
      })
  }

  // -----------IMAGE FULLSCREEN---------------------
  openDialog(data: any) {
    this.dialog.open(ImageDialogComponent, {
      data: { image: data }
    });
  }

  // -----------HANDLE FILE UPLOAD----------------
  onFileChange(event: any) {
    const reader = new FileReader();
    reader.onload = (e: any) => {
      const text = e.target.result;
      console.log(text);
    };
    reader.readAsText(event.target.files[0]);
  }

  fileBrowseHandler(imgFile: any) {
    this.selectedImage = ''
    this.files = []
    // this.browseFilesLenth = imgFile.target.files.length;
    // to validate file SAST
    const allowedTypes = ['application/dicom'];
    for(let i =0; i< this.files.length; i++){
      if (!allowedTypes.includes(this.files[i].type)) {
        this._snackBar.open('Please upload valid file', 'Close', {
          duration: 2000,
        });
        this.files = []
        return ;
      }
    }
    this.prepareFilesList(imgFile.target.files);
    this.demoFile = this.files;
    this.file = this.files[0];
    console.log(this.demoFile)
    this.preview = false;
    this.form.setValue(this.files);
    // this.uploadDocument(this.file);
    //  console.log("on choosing")
  }

  prepareFilesList(files: Array<any>) {
    for (const item of files) {
      const cleanedName = item.name.replace(/\[object Object\]/g, '');
      const newFile = new File([item], cleanedName, { type: item.type });
      this.files.push(newFile);
    }
    console.log("PREPRARE", this.files)
    this.uploadFilesSimulator(0, files);
  }
  uploadFilesSimulator(index: number, files: any) {
    setTimeout(() => {
      console.log(this.files)
      console.log("START TIMEOUT")
      if (index === this.files.length) {
        console.log("RETURN")
        return;
      } else {
        this.files[index].progress = 0;
        const progressInterval = setInterval(() => {
          if (this.files[index].progress >= 100) {
            clearInterval(progressInterval);
            this.loadDICOMImages(this.files[0], 1, 4)
            // this.uploadFilesSimulator(index + 1,files);
          } else {
            this.files[index].progress += 10;
          }
        }, 200);
      }
    }, 1000);
  }

  cancelUpload() {
    this.files = [];
    this.Reset()
  }

  // -----------HANDLE ON SUBMIT---------------------
  Submit() {
    if (this.form.invalid) {
      this.snackBar.open('Please select a File before Submitting', '✖', {
        horizontalPosition: 'center',
        verticalPosition: 'top',
        duration: 3000,
      });
      return;
    }
    this.spinner = true
    const regex = /^(.*\.dcm$).*/
    if (this.demoFile.length == 0) {
      // this.validationLabelSelectImage = "Select a DICOM file to proceed";
      console.log("EMPTY")
    }
    else {
      for (let i = 0; i < this.demoFile.length; i++) {
        const fileData = new FormData();
        this.selectedFile = this.demoFile[i];
        const isMatch = regex.test(this.selectedFile.name)
        if (!isMatch) {
          console.log("HEY")
          // this.val = false
          // this.labelCheck = "* Allowed Files Extensions are .dcm"
        } else {
          console.log(this.selectedFile.name);
          // this.showSpinner1 = true;
          fileData.append('payload', this.selectedFile);
          this.dicomService.api(this.dicomUrl, fileData).subscribe((res) => {
            console.log(res)
            // this.showSpinner1 = false
            this.res1 = this.sanitizeImage(res.original);
            this.table = true
            this.spinner = false
            // this.imagePath = this.res1;
            this.res2 = this.sanitizeImage(res.anonymize)
          }, error => {
            this.handleError(error)
          })
        }
      }
    }
  }

  // -----------HANDLE ON RESET---------------------
  Reset() {
    console.log("RESET CALLED")
    // window.location.reload();
    this.preview = false;
    this.files = [];
    this.demoFile = [];
    this.selectedFile = "";
    this.selectedImage = "";
    this.table = false;
    this.spinner = false;
    this.dicom = false
    this.dicomFile = []
    this.onclick(this.dicom1);
    this.onclick(this.dicom2);
    this.onclick(this.dicom3);
  }
  sanitizeImage(imageData: string): SafeUrl {
    return this.sanitizer.bypassSecurityTrustUrl('data:image/jpg;base64,' + imageData);
  }
}
