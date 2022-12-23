import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie';

@Injectable({
  providedIn: 'root'
})
export class ProjectServiceService {

  constructor(
    private http: HttpClient,
    private router: Router,
    private cookieService: CookieService
  ) {}


  myURL = `//127.0.0.1:8000/api/projects`;

  getProjects(){
   return this.http.get(this.myURL).subscribe((data)=>{
    console.log(data);
    
   })
  }


}
