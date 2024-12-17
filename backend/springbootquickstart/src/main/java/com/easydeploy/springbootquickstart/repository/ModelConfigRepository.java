package com.easydeploy.springbootquickstart.repository;

import com.easydeploy.springbootquickstart.model.ModelConfig;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;


//继承JpaRepository<ModelConfig, Long>存在一些默认函数
//1、保存和更新方法：
//save(S entity): 保存或更新一个实体。
//saveAll(Iterable<S> entities): 保存或更新多个实体。
//2、删除方法：
//deleteById(ID id): 根据 ID 删除实体。
//delete(T entity): 删除一个实体。
//deleteAll(): 删除所有实体。
//deleteAll(Iterable<? extends T> entities): 删除多个实体。
//3、查询方法：
//findById(ID id): 根据 ID 查询实体。
//findAll(): 查询所有实体。
//findAllById(Iterable<ID> ids): 根据多个 ID 查询实体。
//count(): 返回实体总数。
//existsById(ID id): 检查某个 ID 的实体是否存在。
//4、分页和排序方法：
//findAll(Sort sort): 根据指定排序规则查询所有实体。
//findAll(Pageable pageable): 分页查询所有实体。


@Repository
public interface ModelConfigRepository extends JpaRepository<ModelConfig, Long> {

    // 根据用户查找配置
    List<ModelConfig> findByUser_UserId(int userId);

}