/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { environment } from 'src/environments/environment';
import { ImageDialogComponent } from '../image-dialog/image-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { NonceService } from '../nonce.service';

@Component({
  selector: 'app-semi-structured-text',
  templateUrl: './semi-structured-text.component.html',
  styleUrls: ['./semi-structured-text.component.css']
})
export class SemiStructuredTextComponent implements OnInit{
  selectType:any = 'Privacy';
  selectValue: string = '';
  files: any[] = [];
  demoFile: any[] = [];
  selectedFile: File | any;
  file: File | any;
  form: FormGroup;
  ocrvalue: string = 'Tesseract';
  ocr_options = ['Tesseract', 'EasyOcr', 'ComputerVision'];
  portfolioName_value = '';
  accountName_value = '';
  exclusionList_value = '';
  filePreview: any = '';
  private url :any;
  pdfSrc: SafeResourceUrl | null = null;
  output : boolean = false;
  spinner : boolean = false;
  sampleImg = environment.imagePathurl + '/assets/image/Doc.png';
  sampleFile = environment.imagePathurl + '/assets/samplefiles/Healthcare_Application.pdf';
  sampleFile2 = environment.imagePathurl + '/assets/samplefiles/Life_Insurance.pdf';

  constructor(private fb: FormBuilder,  public dialog: MatDialog,  public _snackBar: MatSnackBar, private https: HttpClient, private sanitizer: DomSanitizer,public nonceService:NonceService) {
    this.form = this.fb.group({
      languageModel: ['', Validators.required],
    });
  }
  ngOnInit() {
    let ip_port: any;
    ip_port = this.getLocalStoreApi();
    this.setApilist(ip_port);
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
  setApilist(ip_port: any) {
    this.url = ip_port.result.Privacy + ip_port.result.Privacy_Pdf;  
   }

  resetAll() {
    this.portfolioName_value = '';
    this.accountName_value = '';
    this.exclusionList_value = '';
    this.output = false;
    this.spinner = false;
    this.removeFile();
  }
  removeFile() {
    this.demoFile = [];
    this.files = [];
  }
  submit() {
    this.getSelectedValues();
    this.output = false;
    if (this.ocrvalue === '') {
      {
        this.openSnackBar('Please select a Language Model before submitting', 'Close');
      }
      return;
    }
    if (this.files.length === 0) {
      this.openSnackBar('Please upload a file before submitting', 'Close');
      return
    }
    this.spinner = true;
    const formData = new FormData();
    formData.append('pdf', this.demoFile[0]); 
    formData.append('portfolio', this.portfolioName_value);
    formData.append('account', this.accountName_value);
    formData.append('exclusionList', this.exclusionList_value);
  
    this.https.post(`${this.url}?ocrvalue=${encodeURIComponent(this.ocrvalue)}`, formData, { responseType: 'blob' }).subscribe(
      response => {
        console.log('Upload successful', response);
        const blob = new Blob([response], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob); 
        this.pdfSrc = this.sanitizer.bypassSecurityTrustResourceUrl(url); 
        this.output = true;
        this.spinner = false;
      },
      error => {
        let errorMessage = 'API Failed';
        if (error.error instanceof Blob) {
          error.error.text().then((text: string) => {
            try {
              const errorJson = JSON.parse(text);
              if (errorJson.detail === 'Portfolio/Account Is Incorrect') {
                errorMessage = errorJson.detail;
              }
            } catch (e) {
            }
            this.openSnackBar(errorMessage, 'Close');
          });
        } else {
          if (error.error?.detail === 'Portfolio/Account Is Incorrect') {
            errorMessage = error.error.detail;
          }
          this.openSnackBar(errorMessage, 'Close');
        }
        this.openSnackBar(errorMessage, 'Close');
        this.spinner = false;
        this.output = false;
      }
    );
  }
  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, '✖', {
      duration: 3000,
      horizontalPosition: 'center',
      verticalPosition: 'top',
      panelClass: ['le-u-bg-black'],
    });
  }
  selectOptionOcr(e: any) {
    console.log('Selected option ID:', e.value);
    this.ocrvalue = e.value;
  }

  handleSelectTypeChange(){
      this.selectValue = '';
  }

  onFileChange(event: any) {
    const reader = new FileReader();
    reader.onload = (e: any) => {
      const text = e.target.result;
      console.log(text);
    };
    reader.readAsText(event.target.files[0]);
  }

  fileBrowseHandler(File: any) {
    console.log(File.target.files);
    this.prepareFilesList(File.target.files);
    this.demoFile = this.files;
    this.file = this.files[0];
        // to validate file SAST
        const allowedTypes = ['application/pdf'];
        for(let i =0; i< this.file.length; i++){
          if (!allowedTypes.includes(this.file[i].type)) {
            this._snackBar.open('Please upload valid file', 'Close', {
              duration: 2000,
            });
            this.file = [];
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
  uploadSampleFile(fileType: string) {
    const fileToFetch = fileType === 'sampleFile' ? this.sampleFile : this.sampleFile2;
  
    fetch(fileToFetch)
        .then(response => response.blob())
        .then(blob => {
            const fileName = fileToFetch.split('/').pop() || 'sample_document.pdf';
            const samplePdf = new File([blob], fileName, { type: "application/pdf" });
            const event = { target: { files: [samplePdf] } };
            this.onFileChange(event);
            this.fileBrowseHandler(event);
        })
        .catch(error => {
        });
  }
  openDialog(data: any) {
    this.dialog.open(ImageDialogComponent, {
      data: { pdf: data, flag: true },
      backdropClass: 'custom-backdrop'
    });
    console.log("data", data)
  }
  getSelectedValues(): void {
    this.portfolioName_value = localStorage.getItem('selectedPortfolio') ?? '';
    this.accountName_value = localStorage.getItem('selectedAccount') ?? '';
    console.log('Selected Portfolio:', this.portfolioName_value);
    console.log('Selected Account:', this.accountName_value);
  }
}
