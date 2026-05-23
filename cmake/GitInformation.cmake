function(get_git_hash)
    execute_process(
            COMMAND git log -1 --format=%h
            WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
            OUTPUT_VARIABLE HASH
            OUTPUT_STRIP_TRAILING_WHITESPACE
    )

    set(GIT_HASH ${HASH} PARENT_SCOPE)
endfunction()
