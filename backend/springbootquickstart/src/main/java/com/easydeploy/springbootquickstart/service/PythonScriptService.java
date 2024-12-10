package com.easydeploy.springbootquickstart.service;

import java.io.IOException;
import java.util.concurrent.CompletableFuture;

import com.jcraft.jsch.JSchException;

public interface PythonScriptService {

    CompletableFuture<Process> executeTrainingScript(String[] args) throws IOException;

    CompletableFuture<Process> executePredictionScript(String[] args) throws IOException;

    boolean checkCondaEnvironment();

    byte[] downloadFileFromServer(String remoteFilePath) throws JSchException, IOException;
}
