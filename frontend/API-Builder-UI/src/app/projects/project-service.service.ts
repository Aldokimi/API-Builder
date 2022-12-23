import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie';
import { tap } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProjectServiceService {
  constructor(
    private http: HttpClient,
    private router: Router,
    private cookieService: CookieService
  ) {}

  myURL = `//127.0.0.1:8000/api/projects/`;

  getProjects() {
    return this.http.get(this.myURL).pipe(tap((data) => {}));
  }

  getProject(id: string) {
    return this.http.get(`${this.myURL}${id}`).pipe(
      tap((data) => {
        console.log(data,44444);
      })
    );
  }


  addProject(name: any,fileType: any,content: any,owner: any){
    
    const payload = {"name": name ,"file_type": fileType, "file_content": content,"owner":owner };
    console.log(JSON.stringify(payload));

    const httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    }    
    return this.http
      .post<any>(`${this.myURL}`, JSON.stringify(payload), httpOptions,)
      .pipe(
        tap((data) => {
          
        })
      );
  }


}
