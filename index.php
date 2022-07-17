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
<?php if(isset($result)) : ?>
<div class="artikkel">
<a href="<?php echo $result?>"> Artikkel saadaval siin</a>
    </div>
<?php endif;?>

<a href="https://github.com/MarkusKuuse/Paywall" class="git-link">Kood githubis</a>

</body>
</html>