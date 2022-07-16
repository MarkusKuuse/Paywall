<?php

if(isset($_POST["link"])) {
    $link = $_POST["link"];
    $command = escapeshellcmd("python Bypass.py $link");
    $result = shell_exec($command);
    echo $result;
    echo $link;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>EPIC WIN</title>
</head>
<body>
<form action="index1.php" method="post">
    <label for="link">Delfi artikkel:  </label>
    <input type="text" id="link" name="link">
    <input type="submit" value="Saada" >

</form>
<a href="<?php if(isset($result)){echo $result; }?>"> Artikkel saadaval siin</a>
</body>
</html>