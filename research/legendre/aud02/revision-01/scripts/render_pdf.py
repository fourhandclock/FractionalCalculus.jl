"""Render a primary-source page with already installed Poppler/Cairo libraries."""
import ctypes as C,ctypes.util,sys
from pathlib import Path
p=C.CDLL(ctypes.util.find_library('poppler-glib'));c=C.CDLL(ctypes.util.find_library('cairo'))
p.poppler_document_new_from_file.argtypes=[C.c_char_p,C.c_char_p,C.c_void_p];p.poppler_document_new_from_file.restype=C.c_void_p
p.poppler_document_get_page.argtypes=[C.c_void_p,C.c_int];p.poppler_document_get_page.restype=C.c_void_p
p.poppler_page_get_size.argtypes=[C.c_void_p,C.POINTER(C.c_double),C.POINTER(C.c_double)]
p.poppler_page_render.argtypes=[C.c_void_p,C.c_void_p]
c.cairo_image_surface_create.argtypes=[C.c_int,C.c_int,C.c_int];c.cairo_image_surface_create.restype=C.c_void_p
c.cairo_create.argtypes=[C.c_void_p];c.cairo_create.restype=C.c_void_p
c.cairo_scale.argtypes=[C.c_void_p,C.c_double,C.c_double]
c.cairo_set_source_rgb.argtypes=[C.c_void_p,C.c_double,C.c_double,C.c_double]
c.cairo_paint.argtypes=[C.c_void_p]
c.cairo_surface_write_to_png.argtypes=[C.c_void_p,C.c_char_p];c.cairo_surface_write_to_png.restype=C.c_int
doc=p.poppler_document_new_from_file(Path(sys.argv[1]).resolve().as_uri().encode(),None,None);assert doc
page=p.poppler_document_get_page(doc,int(sys.argv[2]));assert page
w=C.c_double();h=C.c_double();p.poppler_page_get_size(page,C.byref(w),C.byref(h))
surface=c.cairo_image_surface_create(0,int(1.6*w.value),int(1.6*h.value))
ctx=c.cairo_create(surface);c.cairo_set_source_rgb(ctx,1,1,1);c.cairo_paint(ctx);c.cairo_scale(ctx,1.6,1.6)
p.poppler_page_render(page,ctx)
assert c.cairo_surface_write_to_png(surface,str(sys.argv[3]).encode())==0
print('Rendered page index',sys.argv[2],'using existing system libraries.')
