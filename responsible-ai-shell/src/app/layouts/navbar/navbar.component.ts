/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, Inject, OnInit } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { SessionStorageService } from 'ngx-webstorage';

//import { VERSION } from '../../../app/app.constants';
//import { LANGUAGES } from '../../../app/config/language.constants';
import { Account } from '../../../app/core/auth/account.model';
import { AccountService } from '../../../app/core/auth/account.service';
import { LoginService } from '../../../app/login/login.service';
import { ProfileService } from '../../../app/layouts/profiles/profile.service';
import { EntityNavbarItems } from '../../../app/entities/entity-navbar-items';
//import { DOCUMENT } from '@angular/common';
//import { LoginModalService } from '../../core/login/login-modal.service';

// for azure ad login
import { MsalBroadcastService, MsalService } from '@azure/msal-angular';
import { InteractionStatus } from '@azure/msal-browser';
import { filter, takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';
import { RegisterService } from 'src/app/account/register/register.service';
import { EMAIL_ALREADY_USED_TYPE, LOGIN_ALREADY_USED_TYPE } from '../../../app/config/error.constants';
import { EventMessage, EventType, AuthenticationResult } from '@azure/msal-browser';
import { HttpErrorResponse } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { MatSnackBar } from '@angular/material/snack-bar';
import { FormGroup, FormControl, Validators} from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { urlList } from 'src/app/utils/urlList';
import { NonceService } from 'src/app/nonce.service';
import { UserValidationService } from 'src/app/user-validation.service';

@Component({
  selector: 'jhi-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {
  // for sso
  private readonly _destroying$ = new Subject<void>();
  ip_port:any
  raiKabanUrl:any

  inProduction?: boolean;
  isNavbarCollapsed = true;
 // languages = LANGUAGES;
  openAPIEnabled?: boolean;
  version = '';
  account: Account | null = null;
  entitiesNavbarItems: any[] = [];
  loggedIn = false;
  // for sso
  doNotMatch = false;
  error = false;
  errorEmailExists = false;
  errorUserExists = false;
  success = false;
  authenticationError = false;
  roles: any;
  pages: any;
  csrfToken: string;


  constructor(
   // @Inject(DOCUMENT) private document: Document,
    private loginService: LoginService,
    private translateService: TranslateService,
    private sessionStorageService: SessionStorageService,
    private accountService: AccountService,
    private profileService: ProfileService,
    private router: Router,
    private msalBroadcastService: MsalBroadcastService,
    private authService: MsalService,
    private registerService: RegisterService,
    public _snackBar: MatSnackBar,
    private http: HttpClient,
    public nonceService:NonceService,
    public validationService: UserValidationService
  ) //private loginModalService: LoginModalService
  {
    this.csrfToken = this.nonceService.getNonce();

    this.AccountFormCall();

    // if (VERSION) {
    //   this.version = VERSION.toLowerCase().startsWith('v') ? VERSION : `v${VERSION}`;
    // }
  }
//   goToUrl(): void {
//     this.document.location.href = 'http://vimptblt155:5601/app/dashboards#/view/0adcb4d0-40c7-11ee-812b-b1392db18755?_g=(filters:!())';
// }

goToUrl(){
  if(localStorage.getItem("res") != null){
    const x = localStorage.getItem("res")
    if(x != null){

      this.ip_port = JSON.parse(x)

    }
  }
}

  ngOnInit(): void {
    this.clearLocalStorage();
    this.getAllAccountData();
    if(environment.isSSO) {
      console.log("MSAL SERVICE INIT")
       this.msalBroadcastService.inProgress$
      .pipe(
        filter((status: InteractionStatus) => status === InteractionStatus.None),
        takeUntil(this._destroying$)
      )
      .subscribe(() => {
        this.setLoginDisplay();
        console.log("SET LOGIN DISPLAY METHOD ACTIVATED")
      });

    window.onscroll = () => {
      this.scrollFunction();
    };
    if(localStorage.getItem('mail') != null){
      const mail = localStorage.getItem('mail');
     if(mail)
     console.log("executing based on local storage");
     this.register();
    }
    }



    this.entitiesNavbarItems = EntityNavbarItems;
    // this.profileService.getProfileInfo().subscribe(profileInfo => {
    //   this.inProduction = profileInfo.inProduction;
    //   this.openAPIEnabled = profileInfo.openAPIEnabled;
    // });

    this.accountService.getAuthenticationState().subscribe(account => {
      this.account = account;
    });
    this.getInitials();
  }

  changeLanguage(languageKey: string): void {
    this.sessionStorageService.store('locale', languageKey);
    this.translateService.use(languageKey);
  }

  collapseNavbar(): void {
    this.isNavbarCollapsed = true;
    this.reloadShell();
    }

  reloadShell(): void{
// Subscribe to route changes
this.router.events.subscribe(event => {
  if (event instanceof NavigationEnd) {
    // Reload the page
    location.reload();
  }
});

  }
  isAuthenticated(): boolean {

   //return this.accountService.isAuthenticated();

    if(sessionStorage.getItem('jhi-authenticationToken') || localStorage.getItem('jhi-authenticationToken')){
     return true;
    }else{
      return false;
    }
  }

  loginNavbar(): void {
    // this.loginModalService.open();
    this.router.navigate(['/login']);
    console.log('1');
  }

  logout(): void {
    this.collapseNavbar();
    this.loginService.logout();
    // this.loginModalService.open();
    this.router.navigate(['/login']);
    localStorage.clear();

  }

  toggleNavbar(): void {
    this.isNavbarCollapsed = !this.isNavbarCollapsed;
  }
  getImageUrl(): string {
    return this.isAuthenticated() ? this.accountService.getImageUrl() : '';
  }
  scrollFunction(): void {
    const backToTop = document.getElementById('back_to_top') as HTMLElement;
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      backToTop.style.display = 'block';
    } else {
      backToTop.style.display = 'none';
    }
  }
  setLoginDisplay(): void {
    console.log("in set login display");
    this.loggedIn = this.authService.instance.getAllAccounts().length > 0;
    if (this.loggedIn) {
      console.log('inside if logged In: ', new Date());
      const id = this.authService.instance.getAllAccounts()[0].username;
      const index = id.indexOf('@');
      localStorage.setItem('mail', id.substring(0, index) + '@infosys.com');
      this.register();
    }
    // else {
    //   this.loginService.logout();
    // }
  }
  register(): void {
    console.log("register from navbar");
    this.doNotMatch = false;
    this.error = false;
    this.errorEmailExists = false;
    this.errorUserExists = false;
    const userName = (window && window.localStorage && typeof localStorage !== 'undefined') ? localStorage.getItem('mail')! :'{}'
    const valid = this.validationService.isValidEmail(userName) || this.validationService.isValidName(userName)

    const cred =  urlList.user_cred;
    if (cred !==  urlList.user_cred && !valid) {
      this.doNotMatch = true;
    } else {
      const login = userName;
      const email = userName;
      this.registerService.save({ login, email, cred, langKey: 'en' }).subscribe(
       () => (this.success = true),
       response => this.processError(response),// modified backend to make this work
       ()=> this.login()

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
   login(): void {
    console.log("IN LOGIN of navbar")
    localStorage.setItem('userName', localStorage.getItem('mail') || '{}');
    let user;
    if(this.validationService.isValidEmail(localStorage.getItem('mail')) || this.validationService.isValidName(localStorage.getItem('mail'))){
      user = localStorage.getItem('mail')
    }
    this.loginService
      .login({
        username: user || '{}',
        cred: urlList.user_cred,
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
          localStorage.setItem("userid",JSON.stringify(res.login));

          this.roles = res.authorities;
          console.log("ROLES FROM LOCAL STORAGE" + this.roles)

          this.loginService.getPages(this.roles)
            .then(pages => {
            this.pages = pages;
            console.log(this.pages)
          });

          // this needs to be called once successfully logsin
          this.msalBroadcastService.msalSubject$
          .pipe(
            filter(
              (msg: EventMessage) =>
                msg.eventType === EventType.LOGIN_SUCCESS
            )
          )
          .subscribe((result: EventMessage) => {
            const payload = result.payload as AuthenticationResult;
            this.authService.instance.setActiveAccount(
              payload.account
            );
          });

        },
        () => (this.authenticationError = true)
      );
   }
   getInitials(): string {
    return this.isAuthenticated() ? this.accountService.getUserNames():'U';
  }

  callCount: number = 0; 
  portfolioSelected=false
  Accountselected=false
  Portfolio_options=[]
  Account_options=[]
  accountDetail: any;
  portfolioArr :any =[]
  AccountForm!: FormGroup;
  portfolioUrl= 'http://localhost:<YOUR_ADMIN_PORT>/api/v1/rai/admin/getAccount';

  AccountFormCall(){
    this.AccountForm = new FormGroup({
      portfolio: new FormControl('Portfolio Name', [Validators.required]),
      account: new FormControl('Account Name', [Validators.required]),
    });
  }

  getAllAccountData(){
    this.http.get( this.portfolioUrl).subscribe
        ((res: any) => {
          console.log("res=========>>>",res[0].AccountDetails)
          
          this.accountDetail=res[0].AccountDetails
          for(let i=0;i<res[0].AccountDetails.length;i++){
            console.log("portfolio",res)
            const portfolio = res[0].AccountDetails[i].portfolio
            console.log("portfolio11111",portfolio)
            this.portfolioArr.push(portfolio)
          }
          this.Portfolio_options = this.portfolioArr
          console.log("portfolio",this.portfolioArr)
        }, error => {
            const message = (error.error && (error.error.detail || error.error.message)) || "The Api has failed"
            const action = "Close"
            this._snackBar.open(message, action, {
              duration: 3000,
              horizontalPosition: 'left',
              panelClass: ['le-u-bg-black'],
            });
        })
   }

  accountDropDown(){
    this.callCount++
    this.portfolioSelected=true
    const portfolio = this.AccountForm.controls['portfolio'].value
    if (portfolio === 'Portfolio Name') {
      localStorage.removeItem('selectedPortfolio');
      return;
    }
    localStorage.setItem('selectedPortfolio', portfolio);
    console.log("inside accountDrop===",portfolio)
    const accountArr: any = [];
    for(let i=0;i<this.accountDetail.length;i++){
      if(this.accountDetail[i].portfolio == portfolio){
        accountArr.push(this.accountDetail[i].account )
      }
    }
    this.Account_options = accountArr
    if (this.callCount > 1) {
      this.AccountForm.get('account')?.setValue(this.Account_options[0]);
      // this.AccountForm.get('account')?.reset();
      this.Accountselected = true
    }

  }
  activateSubcommands(){

    this.Accountselected = true
    const account = this.AccountForm.controls['account'].value;
    if (account === 'Account Name') {
      localStorage.removeItem('selectedAccount');
      return;
    }
    localStorage.setItem('selectedAccount', account);
    if(this.AccountForm.valid){
      //this.openRightSideModal4(this.AccountForm.value)
    }else{
      this._snackBar.open("Please select an Account and Portfolio", "Close", {
        duration: 3000,
        horizontalPosition: 'left',
        panelClass: ['le-u-bg-black'],
      });
    }
  }
  clearLocalStorage(): void {
    localStorage.removeItem('selectedPortfolio');
    localStorage.removeItem('selectedAccount');
  }
}
