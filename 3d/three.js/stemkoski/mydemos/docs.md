



```js
// 绘制立方体
function TestCube(){
  const geometry = new THREE.BoxGeometry( 1, 1, 1 );
  const material = new THREE.MeshBasicMaterial( {color: 0x00ff00} );
  const cube = new THREE.Mesh( geometry, material );
  scene.add( cube );
  
  const lineSegments = DashLinesBoxTool.createDashLinesBox( 1,1,1,"#ff0000",0.1,0.1 );
  
  objects.push( lineSegments );
  cube.add( lineSegments );
}

// 绘制球形
function TestSphere(){
  const geometry = new THREE.SphereGeometry( 1, 32, 16 );
  const material = new THREE.MeshBasicMaterial( { color: 0x339966 } );
  const sphere = new THREE.Mesh( geometry, material );
  sphere.position.set(2,0,0)
  scene.add( sphere );
  
  const lineSegments = DashLinesBoxTool.createDashLinesBoxWithObject( sphere,"#ff0000",0.1,0.1 );
  
  objects.push( lineSegments );
  sphere.add( lineSegments );
}

// 绘制圆环
function TestTorus(){
  const geometry = new THREE.TorusGeometry( 1, 0.5, 16, 100 );
  const material = new THREE.MeshBasicMaterial( { color: 0xff0077 } );
  const torus = new THREE.Mesh( geometry, material );
  torus.position.set(-3,0,0)
  scene.add( torus );
  
  const lineSegments = DashLinesBoxTool.createDashLinesBoxWithObject( torus,"#ff0000",0.1,0.1 );
  
  objects.push( lineSegments );
  torus.add( lineSegments );
}

// 绘制扭曲圆环
function TestTorusKnot(){
  const geometry = new THREE.TorusKnotGeometry( 0.8, 0.2, 100, 16 );
  const material = new THREE.MeshBasicMaterial( { color: 0xff4400 } );
  const torusKnot = new THREE.Mesh( geometry, material );
  torusKnot.position.set(0,3,0)
  scene.add( torusKnot );
  
  
  const lineSegments = DashLinesBoxTool.createDashLinesBoxWithObject( torusKnot,"#ff0000",0.1,0.1 );
  objects.push( lineSegments );
  torusKnot.add( lineSegments );
}

```



