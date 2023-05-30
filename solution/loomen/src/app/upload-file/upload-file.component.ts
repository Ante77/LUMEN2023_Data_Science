import { Component, OnInit } from '@angular/core';
import { FileUploadService } from './file-upload.service';

@Component({
	selector: 'app-file-upload',
	templateUrl: './upload-file.component.html',
	styleUrls: ['./upload-file.component.css']
})
export class FileUploadComponent implements OnInit {

	// Variable to store shortLink from api response
	shortLink: string = "";
	loading: boolean = false; // Flag variable
	file: File | null = null; // Variable to store file
	instruments: any | null = null;
	instrumentsArr: string[] | null = null;
	processing: boolean = false;

	// Inject service
	constructor(private fileUploadService: FileUploadService) { }

	ngOnInit(): void {
		this.fileUploadService.instrumentsObservable.subscribe(
			(data) => {
				this.instruments = data;
				this.instrumentsArr = [];
				
				if(this.instruments['cel'] == 1)
					this.instrumentsArr.push('čelo');
				if(this.instruments['cla'] == 1)
					this.instrumentsArr.push('klarinet');
				if(this.instruments['gac'] == 1)
					this.instrumentsArr.push('akustična gitara');
				if(this.instruments['gel'] == 1)
					this.instrumentsArr.push('električna gitara');
				if(this.instruments['pia'] == 1)
					this.instrumentsArr.push('klavir');
				if(this.instruments['tru'] == 1)
					this.instrumentsArr.push('truba');
				if(this.instruments['vio'] == 1)
					this.instrumentsArr.push('violina');
				if(this.instruments['voi'] == 1)
					this.instrumentsArr.push('ljudski glas');
				if(this.instruments['flu'] == 1)
					this.instrumentsArr.push('frula');
				if(this.instruments['org'] == 1)
					this.instrumentsArr.push('orgulje');
				if(this.instruments['sax'] == 1)
					this.instrumentsArr.push('saksofon');
			}
		);

		this.fileUploadService.processingObservable.subscribe(
			(data) => this.processing = data
		);
	}

	// On file Select
	onChange(event: Event) {
    if (!event.target) return;
		this.file = (event.target as HTMLInputElement).files![0];
	}

	// OnClick of button Upload
	onUpload() {
		this.loading = !this.loading;
		console.log(this.file);
		this.fileUploadService.upload(this.file!);
	}
}
