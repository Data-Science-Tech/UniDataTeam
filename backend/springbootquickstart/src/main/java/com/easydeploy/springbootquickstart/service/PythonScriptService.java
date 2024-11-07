package com.easydeploy.springbootquickstart.service;

import java.io.IOException;
import java.util.concurrent.CompletableFuture;

public interface PythonScriptService {

    CompletableFuture<Process> executeTrainingScript(String[] args) throws IOException;

    CompletableFuture<Process> executePredictionScript(String[] args) throws IOException;

    boolean checkCondaEnvironment();
}
