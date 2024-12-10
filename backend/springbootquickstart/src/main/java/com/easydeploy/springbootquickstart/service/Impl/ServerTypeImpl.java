package com.easydeploy.springbootquickstart.service.Impl;

import com.easydeploy.springbootquickstart.model.ServerType;
import com.easydeploy.springbootquickstart.repository.ServerTypeRepository;
import com.easydeploy.springbootquickstart.service.ServerTypeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class ServerTypeImpl implements ServerTypeService {

    @Autowired
    private ServerTypeRepository serverTypeRepository;

    @Override
    public List<ServerType> getAllServerTypes() {
        return serverTypeRepository.findAll();
    }
}
