/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { Component, OnInit, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';

//import { VERSION } from '../../../app/app.constants';
import { AccountService } from '../../../app/core/auth/account.service';
import { LoginService } from '../../../app/login/login.service';
import { ProfileService } from '../../../app/layouts/profiles/profile.service';
declare const $: any;

@Component({
  selector: 'jhi-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss'],
})
export class SidebarComponent implements OnInit, AfterViewInit {
  inProduction?: boolean;
  isNavbarCollapsed = true;
  swaggerEnabled?: boolean;
 // version: string;
  public currentWidth = '250px';
  constructor(
    private loginService: LoginService,
    private accountService: AccountService,
    private profileService: ProfileService,
    private router: Router
  ) {
  //this.version = VERSION ? (VERSION.toLowerCase().startsWith('v') ? VERSION : 'v' + VERSION) : '';
  }

  ngOnInit(): void {
    this.profileService.getProfileInfo().subscribe(profileInfo => {
      this.inProduction = profileInfo.inProduction;
      this.swaggerEnabled = profileInfo.openAPIEnabled;
    });
  }

  ngAfterViewInit(): void {
    $('.linktext').hide();
  }
  collapseNavbar(): void {
    this.isNavbarCollapsed = true;
  }

  isAuthenticated(): boolean {
    return this.accountService.isAuthenticated();
    // return true;
  }

  login(): void {
    this.router.navigate(['/login']);
  }

  logout(): void {
    this.collapseNavbar();
    this.loginService.logout();
    this.router.navigate(['']);
  }

  toggleNavbar(): void {
    this.isNavbarCollapsed = !this.isNavbarCollapsed;
  }

  // getImageUrl(): string {
  //   return this.isAuthenticated() ? this.accountService.getImageUrl() : '';
  // }
}
