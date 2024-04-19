'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_NV_gpu_multicast'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_NV_gpu_multicast',error_checker=_errors._error_checker)
GL_MULTICAST_GPUS_NV=_C('GL_MULTICAST_GPUS_NV',0x92BA)
GL_MULTICAST_PROGRAMMABLE_SAMPLE_LOCATION_NV=_C('GL_MULTICAST_PROGRAMMABLE_SAMPLE_LOCATION_NV',0x9549)
GL_PER_GPU_STORAGE_BIT_NV=_C('GL_PER_GPU_STORAGE_BIT_NV',0x0800)
GL_PER_GPU_STORAGE_NV=_C('GL_PER_GPU_STORAGE_NV',0x9548)
GL_RENDER_GPU_MASK_NV=_C('GL_RENDER_GPU_MASK_NV',0x9558)
@_f
@_p.types(None,)
def glMulticastBarrierNV():pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLbitfield,_cs.GLenum)
def glMulticastBlitFramebufferNV(srcGpu,dstGpu,srcX0,srcY0,srcX1,srcY1,dstX0,dstY0,dstX1,dstY1,mask,filter):pass
@_f
@_p.types(None,_cs.GLbitfield,_cs.GLuint,_cs.GLintptr,_cs.GLsizeiptr,ctypes.c_void_p)
def glMulticastBufferSubDataNV(gpuMask,buffer,offset,size,data):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLbitfield,_cs.GLuint,_cs.GLuint,_cs.GLintptr,_cs.GLintptr,_cs.GLsizeiptr)
def glMulticastCopyBufferSubDataNV(readGpu,writeGpuMask,readBuffer,writeBuffer,readOffset,writeOffset,size):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLbitfield,_cs.GLuint,_cs.GLenum,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLuint,_cs.GLenum,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLint,_cs.GLsizei,_cs.GLsizei,_cs.GLsizei)
def glMulticastCopyImageSubDataNV(srcGpu,dstGpuMask,srcName,srcTarget,srcLevel,srcX,srcY,srcZ,dstName,dstTarget,dstLevel,dstX,dstY,dstZ,srcWidth,srcHeight,srcDepth):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLuint,_cs.GLsizei,arrays.GLfloatArray)
def glMulticastFramebufferSampleLocationsfvNV(gpu,framebuffer,start,count,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLenum,arrays.GLint64Array)
def glMulticastGetQueryObjecti64vNV(gpu,id,pname,params):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLenum,arrays.GLintArray)
def glMulticastGetQueryObjectivNV(gpu,id,pname,params):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLenum,arrays.GLuint64Array)
def glMulticastGetQueryObjectui64vNV(gpu,id,pname,params):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLenum,arrays.GLuintArray)
def glMulticastGetQueryObjectuivNV(gpu,id,pname,params):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLbitfield)
def glMulticastWaitSyncNV(signalGpu,waitGpuMask):pass
@_f
@_p.types(None,_cs.GLbitfield)
def glRenderGpuMaskNV(mask):pass