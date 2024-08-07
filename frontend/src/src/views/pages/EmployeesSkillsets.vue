

<script>
//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 2; // Set the required role for this page
getPageAuthorization(pageRole);

</script>

<template>
  <div className="card">
      <h5>Employee Skillsets</h5>
      <p>Module in Contruction.</p>
  </div>
</template>
