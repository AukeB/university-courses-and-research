# Imports.
import os,requests
import urllib.request
from tqdm import tqdm
from astropy import units as u
import PanSTARRS_query as Pquery
import handy


def authorization():
	"""
	Retrieves username and password from a text document.
	"""
	with open('DR2_user_password.txt','r') as f:
		user,password = list(f)
		user = user.replace('\n','')
		password = password.replace('\n','')
		return (user,password)

class TqdmUpTo(tqdm):
	"""
	Provides `update_to(n)` which uses `tqdm.update(delta_n)`.
	Used for providing a urlretrieve progress bar. Example from the Tqdm
	documentation
	"""
	def update_to(self, b = 1, bsize = 1, tsize = None):
		"""
		b  : int, optional
			Number of blocks transferred so far [default: 1].
		bsize  : int, optional
			Size of each block (in tqdm units) [default: 1].
		tsize  : int, optional
			Total size (in tqdm units). If [default: None] remains unchanged.
		"""
		if tsize is not None:
			self.total = tsize

		self.update(b * bsize - self.n)  # will also set self.n = b * bsize

def download_pointing(url,filename):
	"""
	Download a file from an url and save to a local filename
	"""
	
	block_size = 8192

	with requests.get(url=url,auth=authorization(),stream=True) as r:
		r.raise_for_status()
		content_length = r.headers['Content-length']
		
		# Make a progress bar.
		t = tqdm(total = int(content_length),unit='iB',unit_scale=True,desc='Downloading')

		with open(filename, 'wb') as f:
			for chunk in r.iter_content(chunk_size = block_size):
				if chunk: # filter out keep-alive new chunks
					f.write(chunk)
					# f.flush()
					t.update(len(chunk))

		t.close()

def set_up_download(pointing_dir,pointing):
	url_mosaic = f'https://www.lofar-surveys.org/downloads/DR2/mosaics/{pointing}/mosaic-blanked.fits'
	url_field = f'https://lofar-surveys.org/downloads/DR2/fields/{pointing}/image_full_ampphase_di_m.NS_shift.int.facetRestored.fits'
	local_fname = f'{pointing_dir}/{pointing}.fits'

	try:
		print(f' {pointing} not yet downloaded. Trying to obtain mosaic ...')
		download_pointing(url_mosaic,local_fname)
	except requests.exceptions.HTTPError:
		print(' Mosaic does not exist. Field is downloaded instead ...')
		download_pointing(url_field,local_fname)

def download_panstarrs(panstarrs_dir,ra,dec,cutout_size,rgb_filters='irg'):
	# The RA and DEC used in the filenames.
	f_ra = f'{ra:.2f}'
	f_dec = f'{dec:.2f}'

	# The maximum image size, otherwise the PanSTARRS image becomes very very large.
	max_p_size = 3200 # Maximum.
	plot_bbox = False

	# Get download urls for PanSTARRS image.
	# The size for the PanSTARRS query is in pixels (0.25 arcsec/pixel).
	p_size = int((4 * cutout_size / u.arcsec).to(u.dimensionless_unscaled))

	if max_p_size is not None and p_size > max_p_size:
		print(' Using smaller image size for PanSTARRS.\n')
		p_size = max_p_size
		plot_bbox = True
	p_url = Pquery.geturl(ra,dec,size=p_size,format='fits',filters=rgb_filters)

	# Loop over every url in this list.
	for j in tqdm(range(len(p_url)),desc='Looping over filters'):
		url = p_url[j]

		# Get the filter of the current download url.
		filter = url[::-1].split('.')[2]

		file_name = f'ra={f_ra}_dec={f_dec}_s={p_size}_{filter}' # Without .fits.
		file_path = f'{panstarrs_dir}ra={f_ra}_dec={f_dec}_s={p_size}_{filter}.fits'

		#check if the file is not already downloaded
		if handy.download_file(file_name,panstarrs_dir) == False:
			# Download with progress bar
			with TqdmUpTo(unit = 'B', unit_scale = True, miniters = 1, desc = f' Downloading filter {filter}', disable = False) as t:
					urllib.request.urlretrieve(url,file_path,reporthook=t.update_to)

	return p_size

def main():
	# Change these two parameters if this file is runned directly from terminal.
	project_path = '/home/auke/Downloads' # Download location
	pointing = 'P000+23' # Pointing indentifier.

	set_up_download(project_path,pointing)

if __name__ == '__main__':
	main()

