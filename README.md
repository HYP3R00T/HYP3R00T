<img src="./assets/helmet.gif"/>

# Welcome to My GitHub Profile! 👋

I'm Awesome User, and I love coding and building cool projects. Welcome to my corner of the internet!

<!-- JavaScript magic starts here -->
<script>
  const welcomeMessage = document.querySelector('h1');

  welcomeMessage.addEventListener('mouseover', () => {
    welcomeMessage.style.color = getRandomColor();
  });

  welcomeMessage.addEventListener('mouseout', () => {
    welcomeMessage.style.color = ''; // Reset to default color
  });

  function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }
</script>
<!-- JavaScript magic ends here -->
