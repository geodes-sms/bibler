<?php

/**
BiBler - A software to manage references of scientific articles using BibTeX.
Copyright (C) 2018  Eugene Syriani

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

/**
* Proxy to be used to call the BiBler's webservice at a distance
*/
class BiBlerProxy
{
	private static $instance;
	private static $url;

	private function __construct()	{}

	public function setURL($uri) {
		$this->url=$uri;
	}

	public static function getInstance() {
		if (!$instance) {
			$instance=new BiBlerProxy();
		}
			
			return $instance;
		
		
	}


	private function httpPost($url, $data)
	{

		$ch = curl_init( $url );
		curl_setopt( $ch, CURLOPT_POST, 1);
		curl_setopt( $ch, CURLOPT_POSTFIELDS, urlencode($data));
		curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, 1);
		curl_setopt( $ch, CURLOPT_HEADER, 0);
		curl_setopt( $ch, CURLOPT_RETURNTRANSFER, 1);

		$response = curl_exec( $ch );
	    return $response;
	}

	public function addEntry($data) {
		return $this->httpPost($this->url."addentry/",$data);
	}

	public function getBibtex($data) {
		return $this->httpPost($this->url."getbibtex/",$data);
	}

	public function formatBibtex($data) {
		return $this->httpPost($this->url."formatbibtex/",$data);
	}

	public function previewEntry($data) {
		return $this->httpPost($this->url."previewentry/",$data);
	}

	public function validateEntry($data) {
		return $this->httpPost($this->url."validateentry/",$data);
	}

	public function bibtextobibtex($data) {
		return $this->httpPost($this->url."bibtextobibtex/",$data);
	}

	public function bibtextosql($data) {
		return $this->httpPost($this->url."bibtextosql/",$data);
	}

	public function bibtextocsv($data) {
		return $this->httpPost($this->url."bibtextocsv/",$data);
	}

	public function bibtextohtml($data) {
		return $this->httpPost($this->url."bibtextohtml/",$data);
	}
}