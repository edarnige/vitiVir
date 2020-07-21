<template>
  <footer
    class="footer"
    :class="{ [`footer-${type}`]: type }"
    :data-background-color="backgroundColor"
  >
    <div class="container">
      <nav>
        <ul>
          <li>
            <a href="https://www6.bordeaux-aquitaine.inrae.fr/bfp">
              INRAE UMR 1332 BFP
            </a>
          </li>
          <li>
            <a href="https://apsjournals.apsnet.org/doi/full/10.1094/PBIOMES-07-19-0037-A">
              VirAnnot
            </a>
          </li>
          <li>
            <a href="https://www.plan-deperissement-vigne.fr/recherches/programmes-de-recherche/mycovir">
              MYCOVIR
            </a>
          </li>
          <li>
            <a href="https://www.creative-tim.com/license">
              Licenses
            </a>
          </li>
        </ul>
      </nav>
    </div>
  </footer>
</template>
<script>
export default {
  props: {
    backgroundColor: String,
    type: String
  },
  data() {
    return {
      year: new Date().getFullYear()
    };
  }
};
</script>
<style></style>
