import { useRouter } from 'vue-router';

export function getPageAuthorization(pageRole) {
    const getCookieValue = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    };

    const adminRole = parseInt(getCookieValue('admin'), 10);
    const router = useRouter();

    if (adminRole < pageRole) {
        router.push('/unauthorized');
        return false;
    }

    return true;
}

// Add other functions here and export them as needed
export function anotherFunction() {
    // Function logic
}