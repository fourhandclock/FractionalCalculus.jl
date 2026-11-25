"""Render every final PDF page using existing Poppler/Cairo; no new dependencies."""
import ctypes as C,ctypes.util,json,sys,hashlib
from pathlib import Path
p=C.CDLL(ctypes.util.find_library('poppler-glib'));c=C.CDLL(ctypes.util.find_library('cairo'))
p.poppler_document_new_from_file.argtypes=[C.c_char_p,C.c_char_p,C.c_void_p];p.poppler_document_new_from_file.restype=C.c_void_p
p.poppler_document_get_n_pages.argtypes=[C.c_void_p];p.poppler_document_get_n_pages.restype=C.c_int
p.poppler_document_get_page.argtypes=[C.c_void_p,C.c_int];p.poppler_document_get_page.restype=C.c_void_p
p.poppler_page_get_size.argtypes=[C.c_void_p,C.POINTER(C.c_double),C.POINTER(C.c_double)]
p.poppler_page_render.argtypes=[C.c_void_p,C.c_void_p]
c.cairo_image_surface_create.argtypes=[C.c_int,C.c_int,C.c_int];c.cairo_image_surface_create.restype=C.c_void_p
c.cairo_create.argtypes=[C.c_void_p];c.cairo_create.restype=C.c_void_p
for name in ['cairo_save','cairo_restore','cairo_destroy'] :getattr(c,name).argtypes=[C.c_void_p]
c.cairo_surface_destroy.argtypes=[C.c_void_p]
c.cairo_translate.argtypes=[C.c_void_p,C.c_double,C.c_double]
c.cairo_scale.argtypes=[C.c_void_p,C.c_double,C.c_double]
c.cairo_set_source_rgb.argtypes=[C.c_void_p,C.c_double,C.c_double,C.c_double]
c.cairo_paint.argtypes=[C.c_void_p]
c.cairo_surface_write_to_png.argtypes=[C.c_void_p,C.c_char_p];c.cairo_surface_write_to_png.restype=C.c_int
source=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=False);records=[]
for pdf in sorted(source.glob('*.pdf')):
 doc=p.poppler_document_new_from_file(pdf.resolve().as_uri().encode(),None,None);assert doc
 n=p.poppler_document_get_n_pages(doc);sheets=[]
 for start in range(0,n,4):
  surface=c.cairo_image_surface_create(0,1100,1580);ctx=c.cairo_create(surface)
  c.cairo_set_source_rgb(ctx,1,1,1);c.cairo_paint(ctx)
  for j in range(start,min(start+4,n)):
   page=p.poppler_document_get_page(doc,j);assert page
   w=C.c_double();h=C.c_double();p.poppler_page_get_size(page,C.byref(w),C.byref(h))
   c.cairo_save(ctx);c.cairo_translate(ctx,10+550*((j-start)%2),10+790*((j-start)//2))
   scale=min(530/w.value,770/h.value);c.cairo_scale(ctx,scale,scale);p.poppler_page_render(page,ctx);c.cairo_restore(ctx)
  path=out/(pdf.stem+'-pages-'+str(start+1)+'-'+str(min(n,start+4))+'.png')
  assert c.cairo_surface_write_to_png(surface,str(path).encode())==0
  sheets.append(path.name);c.cairo_destroy(ctx);c.cairo_surface_destroy(surface)
 records.append({'pdf':pdf.name,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':n,'contact_sheets':sheets})
(out/'render-record.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(records,indent=2))
