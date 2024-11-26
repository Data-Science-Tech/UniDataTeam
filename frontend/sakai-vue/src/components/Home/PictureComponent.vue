<template>
  <div class="PictureComponent">
    <div class="left-section">
        <img src="@/assets/ha.png" alt="EZDP Logo" class="logo-3" />
        <h1 class="headintro">The AI community building the future.</h1>
        <p class="des">
          The platform where the machine learning community collaborates on models, datasets, and applications.
        </p>
    </div>
    <div class="right-section">
      <h3>Easy Deploy</h3>

        <div class="startbutton" @click="gotoworkbench">
            Let's deploy!  😀---->
        </div>
    </div>
</div>
</template>

<script>
export default
{
    methods:{
        gotoworkbench() {
        console.log("push workbench")
        this.$router.push('/workbench');
        },
    },
}

</script>


<style>
.PictureComponent {
  display: flex;
  /* background-color: white; */
  color: #fff;
  border-radius: 25px; /* Smooth border */
  margin: 12%;
  margin-top: 3%;
  margin-bottom: 10%;
  height: 70%;
  
}

.left-section {
  flex: 2;
  margin-top: 2%;
  background-color: #121022;
  height: 29vw;
  border-radius: 25px 0 0 25px; /* Left part with rounded corners */
  padding: 10vh;
  transition: 1s;
}

.headintro{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: bolder;
    font-size: 2.5vw;
    transition: 1s;
    width: 80%;
    color: white;
}

.des{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color:grey;
    font-size: 1vw;
    transition: 1s;
    width: 80%;
}

.right-wrapper {
  flex: 3;
  /* overflow: hidden; Ensure no overflow outside the rounded corners */
  /*border-radius: 50px 25px 50px 50px;  Right part with rounded corners */
}

.right-section {
  /*background-color: #040219;*/
  background-image:url(../../assets/right-bg.png);
  transition: 1s;
  padding: 30px;
  transform: skewX(-5deg); /* Adds slight tilt */
  margin-left: -10vw; /* Pulls the section to fill the gap */
  border-radius:5%;
  width: 50%;
}

.right-section h3{
    margin-top: 10%;
    margin-left: 10%;
    font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
    font-size: 4vw;
    font-weight:lighter;
    color: rgb(18, 213, 148);
}



.logo-3{
    height: 40%;
    transition: 1s;
}

.startbutton{
    margin-top: 40%;
    margin-left: 42%;
    font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    font-size: 3vh;
    font-weight: bolder;
    padding: 2ch;
    background-color: rgb(243, 207, 24);
    border: 5px white;
    border-radius: 30px;
    transition: 1s;
}
</style>