import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import { Subject } from 'rxjs';

@Injectable({
providedIn: 'root'
})
export class FileUploadService {
	
private instrumentsSubject: Subject<any> = new Subject<any>();
public instrumentsObservable: Observable<any> = this.instrumentsSubject.asObservable();
baseApiUrl = "http://127.0.0.1:5000/companies";
instruments: Observable<any> = new Observable<object>();

private processing: boolean = false;
private processingSubject: Subject<boolean> = new Subject<boolean>();
public processingObservable: Observable<boolean> = this.processingSubject.asObservable(); 
	
constructor(private http:HttpClient) { }

// Returns an observable
upload(file: File) {
	const formData = new FormData();
		
	// Store form name as "file" with file data
	formData.append("file", file, file.name);

	if(this.processing)
		return;
	
	this.processing = true;
	this.processingSubject.next(true);
	console.log('post');
		
	// Make http post request over api
	// with formData as req
	this.http.post(this.baseApiUrl, formData).subscribe(
		(response: any) => {
			console.log(response);
			this.instrumentsSubject.next(response);
			this.processingSubject.next(false);
			this.processing = false;
		}
	)
}
}
