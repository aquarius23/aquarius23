LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_SRC_FILES += dumpmem.cpp
LOCAL_SHARED_LIBRARIES += liblog
LOCAL_SHARED_LIBRARIES += libutils

LOCAL_MODULE := dumpmem
LOCAL_MODULE_TAGS := optional
include $(BUILD_EXECUTABLE)
