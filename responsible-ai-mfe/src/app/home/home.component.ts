/**  MIT license https://opensource.org/licenses/MIT
”Copyright 2024-2025 Infosys Ltd.”
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
import { HttpClient} from '@angular/common/http'
import { Component, ElementRef, HostListener, Renderer2 } from '@angular/core';
import { HomeService } from './home.service';
import { RoleManagerService } from '../services/role-maganer.service';
import { urlList } from '../urlList';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  master_url = urlList.masterurl;
  authorityAPI = urlList.authorityAPI;
  pages: any;
  constructor(private elementRef: ElementRef,private renderer: Renderer2,public https: HttpClient,private homeService :HomeService,public roleService: RoleManagerService) {
  }
  showSidebar = false;
  showComponent!:string;
  toggleComponents(tabValue:any) {
    this.showComponent =tabValue;
    if (this.showSidebar) {
      this.renderer.removeClass(document.body, 'overflow-hidden');
    }
    this.showSidebar = false;
  }
  toggleSidebar() {
    if (this.showSidebar) {
      this.renderer.removeClass(document.body, 'overflow-hidden');
    }else {
      this.renderer.addClass(document.body, 'overflow-hidden');
    }
    this.showSidebar = !this.showSidebar;
  }
  closeSidebar() {
    if (this.showSidebar) {
      this.renderer.removeClass(document.body, 'overflow-hidden');
    }
    this.showSidebar = false;
  }

  ngOnInit() {
    if (this.roleService.getLocalStoreUserRole() === 'ROLE_ML') {
      this.showComponent="workbench";
    }
    else if( this.roleService.getLocalStoreUserRole() == "ROLE_EMPTY"){
      this.showComponent="newUser";
    }
    else{
      this.showComponent="workbench";
    }
    console.log(this.showComponent,"showComponent")
    this.homeService.getConfigApiList(this.master_url).subscribe
      ((res: any) => {
        localStorage.setItem("res", JSON.stringify(res))
      })

  }

}
