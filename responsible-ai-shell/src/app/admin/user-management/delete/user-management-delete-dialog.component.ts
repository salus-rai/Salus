/**
SPDX-License-Identifier: MIT
Copyright 2024 - 2025 Infosys Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

import { Component } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

import { User } from '../user-management.model';
import { UserManagementService } from '../service/user-management.service';
import { NonceService } from 'src/app/nonce.service';

@Component({
  selector: 'jhi-user-mgmt-delete-dialog',
  templateUrl: './user-management-delete-dialog.component.html',
})
export class UserManagementDeleteDialogComponent {
  user?: User;
  csrfToken: string;


  constructor(private userService: UserManagementService, private activeModal: NgbActiveModal,public nonceService:NonceService) 
  {
    this.csrfToken = this.nonceService.getNonce();
  }

  cancel(): void {
    this.activeModal.dismiss();
  }

  confirmDelete(id: number): void {
    this.userService.delete(id).subscribe(() => {
      this.activeModal.close('deleted');
    });
  }
}