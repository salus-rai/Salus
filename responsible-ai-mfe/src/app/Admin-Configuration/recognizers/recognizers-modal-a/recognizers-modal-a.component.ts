/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { PagingConfig } from 'src/app/_models/paging-config.model';

@Component({
  selector: 'app-recognizers-modal-a',
  templateUrl: './recognizers-modal-a.component.html',
  styleUrls: ['./recognizers-modal-a.component.css'],
})
export class RecognizersModalAComponent {
  constructor(
    public dialogRef: MatDialogRef<RecognizersModalAComponent>,
    public _snackBar: MatSnackBar,
    public https: HttpClient,
    @Inject(MAT_DIALOG_DATA) public data: { id: any; api: any; api2: any }
  ) {
    this.pagingConfig = {
      itemsPerPage: this.itemsPerPage,
      currentPage: this.currentPage,
      totalItems: this.totalItems,
    };
  }

  pagingConfig: PagingConfig = {} as PagingConfig;
  currentPage: number = 1;
  itemsPerPage: number = 5;
  totalItems: number = 0;

  dataSource1: any = [];
  closeDialog() {
    this.dialogRef.close();
  }

  ngOnInit(): void {
    console.log('this data is from parrent', this.data.id);
    this.getItemList(this.data.id, this.data.api);
  }
  getItemList(RecogGrpIdgg: any, api: any) {
    // this.copydataRecogGrpId = ""
    // this.copydataRecogGrpId = RecogGrpIdgg
    this.https.post(api, { RecogId: RecogGrpIdgg }).subscribe(
      (res: any) => {
        console.log(res.DataEntities);
        this.dataSource1 = res.DataEntities;
        this.onTableDataChange(this.currentPage);
      },
      (error) => {
        // You can access status:
        console.log(error.status);
        // console.log(error.error.detail)
        console.log(error);
        const message =
          (error.error && (error.error.detail || error.error.message)) ||
          'The Api has failed';
        const action = 'Close';
        this._snackBar.open(message, action, {
          duration: 3000,
          horizontalPosition: 'left',
          panelClass: ['le-u-bg-black'],
        });
      }
    );
  }

  deleteListEntity(id: any) {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      }),
      body: {
        EntityId: id,
      },
    };
    // this.https.delete(this.admin_pattern_rec_delete_list, { headers }).subscribe
    this.https.delete(this.data.api2, options).subscribe(
      (res: any) => {
        console.log('delete Resonce' + res.status);
        if (res.status === 'True') {
          const message = ' Item Deleted Successfully';
          const action = 'Close';
          this._snackBar.open(message, action, {
            duration: 1000,
            panelClass: ['le-u-bg-black'],
          });
        } else if (res.status === 'False') {
          const message = 'Item Deletion was unsucessful';
          const action = 'Close';
          this._snackBar.open(message, action, {
            duration: 1000,
            panelClass: ['le-u-bg-black'],
          });
        }

        this.getItemList(this.data.id, this.data.api);
      },
      (error) => {
        // You can access status:
        console.log(error.status);
        if (error.status == 430) {
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
          // console.log(error.error.detail)
          console.log(error);
          const message =
            (error.error && (error.error.detail || error.error.message)) ||
            'The Api has failed';
          const action = 'Close';
          this._snackBar.open(message, action, {
            duration: 3000,
            horizontalPosition: 'left',
            panelClass: ['le-u-bg-black'],
          });
        }
      }
    );
  }
  onTableDataChange(event: any) {
    this.currentPage = event;
    this.pagingConfig.currentPage = event;
    this.pagingConfig.totalItems = this.dataSource1.length;
  }
}
