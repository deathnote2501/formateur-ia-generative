<script lang="ts">
  import { goto } from '$app/navigation';

  export let title: string;
  export let subtitle: string | undefined = undefined;
  export let menuItems: Array<{ id: string, text: string, targetSlideId: string | number }>;

  function handleNavigation(targetSlideId: string | number) {
    // Assuming courseId=1 for now, as per the issue description
    goto(`/course/1/slide/${targetSlideId}`);
  }
</script>

<div class="menu-template-slide">
  <h2>{title}</h2>
  {#if subtitle}
    <p class="subtitle">{subtitle}</p>
  {/if}
  <ol>
    {#each menuItems as item (item.id)}
      <li>
        <button on:click={() => handleNavigation(item.targetSlideId)}>
          {item.text}
        </button>
      </li>
    {/each}
  </ol>
</div>

<style>
  .menu-template-slide {
    padding: 2rem;
    text-align: left;
  }

  h2 {
    font-size: 2.5em;
    margin-bottom: 0.5em;
  }

  .subtitle {
    font-size: 1.2em;
    margin-bottom: 1.5em;
    color: #555;
  }

  ol {
    list-style-type: decimal;
    padding-left: 2em; /* Standard padding for ordered lists */
  }

  li {
    margin-bottom: 0.75em;
  }

  button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 0.75em 1.5em;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 1em;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  button:hover {
    background-color: #0056b3;
  }
</style>
