const { createApp } = Vue;

const NCOF_SUBSCRIPTION_URI = "/ETRI_INRS_TEAM/NCOF_Nncof_EventSubscription/1.0.0/subscriptions";

createApp({
  data() {
    return {
      subscriptions: {},
      selectedSubscription: null,
      isModalVisible: false,
      error: null,
    };
  },
  computed: {
    hasSubscriptions() {
      return Object.keys(this.subscriptions).length > 0;
    },
    prettyJson() {
      if (!this.selectedSubscription) return "";
      return JSON.stringify(this.selectedSubscription, null, 2);
    },
  },
  methods: {
    fetchSubscriptions() {
      fetch(NCOF_SUBSCRIPTION_URI)
        .then((response) => {
          if (!response.ok) {
            throw new Error(
              `Network response was not ok (${response.status})`
            );
          }
          return response.json();
        })
        .then((data) => {
          this.subscriptions = data;
        })
        .catch((error) => {
          console.error("Error fetching subscriptions:", error);
          this.error = error.message;
        });
    },
    showModal(subscription) {
      this.selectedSubscription = subscription;
      this.isModalVisible = true;
    },
    hideModal() {
      this.isModalVisible = false;
      this.selectedSubscription = null;
    },
    async unsubscribe(subscriptionId) {
      if (
        !confirm(
          `Are you sure you want to unsubscribe from ${subscriptionId}?`
        )
      ) {
        return;
      }

      const deleteUrl = `/ETRI_INRS_TEAM/NCOF_Nncof_EventSubscription/1.0.0/subscriptions/${subscriptionId}`;
      try {
        const response = await fetch(deleteUrl, {
          method: "DELETE",
        });

        if (response.status === 204) {
          // No Content
          alert(`Successfully unsubscribed from ${subscriptionId}`);
          // Remove the subscription from the local data
          delete this.subscriptions[subscriptionId];
          // Trigger reactivity to update the list
          this.subscriptions = { ...this.subscriptions };
        } else {
          const errorData = await response.json();
          throw new Error(
            errorData.detail ||
            `Failed to unsubscribe: ${response.status}`
          );
        }
      } catch (error) {
        console.error("Error unsubscribing:", error);
        alert(`Error unsubscribing: ${error.message}`);
      }
    },
  },
  mounted() {
    this.fetchSubscriptions();
  },
}).mount("#app");
