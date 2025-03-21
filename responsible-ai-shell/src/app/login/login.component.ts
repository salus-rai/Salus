/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, ViewChild, OnInit, AfterViewInit, ElementRef } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { LoginService } from '../../app/login/login.service';
import { AccountService } from '../../app/core/auth/account.service';
import { environment } from 'src/environments/environment';
('app/core/auth/account.service');
// for azure login
import { MsalService, MsalBroadcastService} from '@azure/msal-angular';
import { EventMessage, EventType, AuthenticationResult } from '@azure/msal-browser';
import { filter } from 'rxjs/operators';
// for register
import { RegisterService } from 'src/app/account/register/register.service';
import { EMAIL_ALREADY_USED_TYPE, LOGIN_ALREADY_USED_TYPE } from '../../app/config/error.constants';
import { HttpErrorResponse } from '@angular/common/http';
import { NonceService } from '../nonce.service';
import { UserValidationService } from '../user-validation.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit, AfterViewInit {
  @ViewChild('username', { static: false })
  username!: ElementRef;
  formBased = true;
  masterUrl =environment.master_url
  authenticationError = false;
  roles: any;
  pages: any;
  loginForm = this.fb.group({
    username: [null, [Validators.required]],
    password: [null, [Validators.required]],
    rememberMe: [false],
  });
  // variables for register
  loggedIn = false;
  doNotMatch = false;
  error = false;
  errorEmailExists = false;
  errorUserExists = false;
  success = false;
  csrfToken: string;

  constructor(
    private authService: MsalService,
    private accountService: AccountService,
    private loginService: LoginService,
    private router: Router,
    private fb: FormBuilder,
    private msalBroadcastService: MsalBroadcastService,
    private registerService: RegisterService,
    public nonceService:NonceService,
    public validationService: UserValidationService
  ) {
    this.csrfToken = this.nonceService.getNonce();
  }

  ngOnInit(): void {
    this.loginService.getConfigApiList(this.masterUrl).subscribe
      ((res: any) => {
        localStorage.setItem("res", JSON.stringify(res))
      })
    if(environment.isSSO){
      this.formBased = false;
      if (this.authService.instance.getAllAccounts().length > 0) {
        console.log("inside if contn. of login cpmt");
        this.loginBySSO();
      } else {
        console.log("Msal redirect happening from login oninit");
        this.authService.loginRedirect();
      }
      if(localStorage.getItem('mail')){
        const mail = localStorage.getItem('mail');
       if( JSON.parse(mail!))
       console.log("executing in login component based on local strg,just checking");
       this.register();
      }
    }else{
    // if already authenticated then navigate to home page
    this.accountService.identity().subscribe(() => {
      if (this.accountService.isAuthenticated()) {
        this.router.navigate(['']);
      }
    });
  }


  }

  ngAfterViewInit(): void {
   // this.username.nativeElement.focus();
  }

  login(): void {
    this.loginService
      .login({
        username: this.loginForm.get('username')!.value,
        cred: this.loginForm.get('password')!.value,
        rememberMe: this.loginForm.get('rememberMe')!.value,
      })
      .subscribe(
        (res:any) => {
          this.authenticationError = false;
          if (!this.router.getCurrentNavigation()) {
            // There were no routing during login (eg from navigationToStoredUrl)
          //  this.router.navigate(['landing']);
           this.router.navigate(['responsible-ui']);
        // this.router.navigate(['']);
          }
          console.log("RES::",res);
          console.log("login response",res.login)
          console.log("login response",res.authorities)

          localStorage.setItem("role",JSON.stringify(res.authorities[0]))
          localStorage.setItem("userid",JSON.stringify(res.login))
          // this.roles = JSON.parse(localStorage.getItem('role') || 'null');
          this.roles = res.authorities;
          console.log("ROLES FROM LOCAL STORAGE" + this.roles)

          this.loginService.getPages(this.roles)
            .then(pages => {
            this.pages = pages;
            console.log(this.pages)
          });

        },
        () => (this.authenticationError = true)
      );


  }

  register(): void {
    console.log("register from login");
    this.doNotMatch = false;
    this.error = false;
    this.errorEmailExists = false;
    this.errorUserExists = false;
    const userName = (window && window.localStorage && typeof localStorage !== 'undefined') ? localStorage.getItem('mail')! :'{}'
    const valid = this.validationService.isValidEmail(userName) || this.validationService.isValidName(userName)

    const cred = 'admin';
    if (cred !== 'admin' && !valid) {
      this.doNotMatch = true;
    } else {
      const login = userName;
      const email = userName;
      this.registerService.save({ login, email, cred, langKey: 'en' }).subscribe(
       () => (this.success = true),
       response => this.processError(response),// modified backend to make this work
       ()=> this.loginBySSO()

      );
    }
  }

  private processError(response: HttpErrorResponse): void {
    if (response.status === 400 && response.error.type === LOGIN_ALREADY_USED_TYPE) {
      this.errorUserExists = true;
    } else if (response.status === 400 && response.error.type === EMAIL_ALREADY_USED_TYPE) {
      this.errorEmailExists = true;
    } else {
      this.error = true;
    }
  }
  loginBySSO(): void {
    console.log("in login of logincomponent")
    localStorage.setItem('userName', localStorage.getItem('mail') || '{}');
     let user;
   if(this.validationService.isValidEmail(localStorage.getItem('mail')) || this.validationService.isValidName(localStorage.getItem('mail'))){
     user = localStorage.getItem('mail')
   }
    this.loginService
      .login({
        username: user || '{}',
        cred: 'admin',
        rememberMe: true,
      })
      .subscribe(
        (res:any) => {
          this.authenticationError = false;
          if (!this.router.getCurrentNavigation()) {
           this.router.navigate(['responsible-ui']);
          }
          console.log("login response",res.login)
          console.log("login response",res.authorities[0])

          localStorage.setItem("role",JSON.stringify(res.authorities[0]))
          localStorage.setItem("userid",JSON.stringify(res.login))
          this.roles = res.authorities;
          console.log("ROLES FROM LOCAL STORAGE" + this.roles)

          this.loginService.getPages(this.roles)
            .then(pages => {
            this.pages = pages;
            console.log(this.pages)
          });

          this.msalBroadcastService.msalSubject$
            .pipe(
              filter(
                (msg: EventMessage) => msg.eventType === EventType.LOGIN_SUCCESS
              )
            )
            .subscribe((result: EventMessage) => {
              const payload = result.payload as AuthenticationResult;
              this.authService.instance.setActiveAccount(payload.account);
            });

        },
        () => (this.authenticationError = true)
      );
  }
}
