<script>
//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 3; // Set the required role for this page
getPageAuthorization(pageRole);

</script>

<template>
  <div className="card">
      <h5>Skillsets</h5>
      <p>Page in Construction.</p>
  </div>
</template>
