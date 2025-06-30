from typing import Dict, List, Set, Optional, Any
from enum import Enum


class DirectedGraph:
    """
    A generic unweighted directed graph data structure.
    Keeps the implementation domain-agnostic for reusability.
    """

    def __init__(self):
        # Dictionary to store vertices and their outgoing edges
        self._adjacency_list: Dict[Any, Set[Any]] = {}
        # Dictionary to store vertex data
        self._vertices: Dict[Any, Any] = {}

    def add_vertex(self, vertex_id: Any, vertex_data: Any = None) -> bool:
        """
        Add a new vertex to the graph.

        Args:
            vertex_id: Unique identifier for the vertex
            vertex_data: Data associated with the vertex

        Returns:
            bool: True if vertex was added, False if it already exists
        """
        if vertex_id in self._vertices:
            return False

        self._vertices[vertex_id] = vertex_data
        self._adjacency_list[vertex_id] = set()
        return True

    def add_edge(self, from_vertex: Any, to_vertex: Any) -> bool:
        """
        Connect one vertex with another vertex (directed edge).

        Args:
            from_vertex: Source vertex
            to_vertex: Destination vertex

        Returns:
            bool: True if edge was added, False if vertices don't exist or edge already exists
        """
        if from_vertex not in self._vertices or to_vertex not in self._vertices:
            return False

        if to_vertex in self._adjacency_list[from_vertex]:
            return False  # Edge already exists

        self._adjacency_list[from_vertex].add(to_vertex)
        return True

    def remove_edge(self, from_vertex: Any, to_vertex: Any) -> bool:
        """
        Remove an edge between two vertices.

        Args:
            from_vertex: Source vertex
            to_vertex: Destination vertex

        Returns:
            bool: True if edge was removed, False if edge doesn't exist
        """
        if from_vertex not in self._vertices or to_vertex not in self._vertices:
            return False

        if to_vertex not in self._adjacency_list[from_vertex]:
            return False

        self._adjacency_list[from_vertex].remove(to_vertex)
        return True

    def list_outgoing_adjacent_vertices(self, vertex: Any) -> List[Any]:
        """
        List all vertices that have incoming edges from the given vertex.

        Args:
            vertex: The vertex to get outgoing adjacencies for

        Returns:
            List of vertex IDs that are adjacent to the given vertex
        """
        if vertex not in self._vertices:
            return []

        return list(self._adjacency_list[vertex])

    def list_incoming_adjacent_vertices(self, vertex: Any) -> List[Any]:
        """
        List all vertices that have outgoing edges to the given vertex.

        Args:
            vertex: The vertex to get incoming adjacencies for

        Returns:
            List of vertex IDs that point to the given vertex
        """
        if vertex not in self._vertices:
            return []

        incoming = []
        for v, adjacents in self._adjacency_list.items():
            if vertex in adjacents:
                incoming.append(v)

        return incoming

    def get_vertex_data(self, vertex_id: Any) -> Any:
        """Get the data associated with a vertex."""
        return self._vertices.get(vertex_id)

    def get_all_vertices(self) -> List[Any]:
        """Get all vertex IDs in the graph."""
        return list(self._vertices.keys())

    def vertex_exists(self, vertex_id: Any) -> bool:
        """Check if a vertex exists in the graph."""
        return vertex_id in self._vertices


class Privacy(Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class Person:
    """
    Domain/Entity class representing a social media user.
    """

    def __init__(self, user_id: str, name: str, gender: str = "",
                 biography: str = "", privacy: Privacy = Privacy.PUBLIC,
                 age: Optional[int] = None, location: str = ""):
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.biography = biography
        self.privacy = privacy
        self.age = age
        self.location = location

    def __str__(self) -> str:
        return f"Person(ID: {self.user_id}, Name: {self.name})"

    def __repr__(self) -> str:
        return self.__str__()

    def get_public_info(self) -> Dict[str, Any]:
        """Get information that's always visible regardless of privacy settings."""
        return {
            "user_id": self.user_id,
            "name": self.name
        }

    def get_full_info(self) -> Dict[str, Any]:
        """Get all profile information."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "gender": self.gender,
            "biography": self.biography,
            "privacy": self.privacy.value,
            "age": self.age,
            "location": self.location
        }


class SocialMediaApp:
    """
    Social media application using the directed graph for managing user connections.
    """

    def __init__(self):
        self.graph = DirectedGraph()
        self.users: Dict[str, Person] = {}

    def add_user(self, person: Person) -> bool:
        """Add a new user to the social media app."""
        if person.user_id in self.users:
            return False

        self.users[person.user_id] = person
        return self.graph.add_vertex(person.user_id, person)

    def follow_user(self, follower_id: str, followee_id: str) -> bool:
        """Make one user follow another."""
        if follower_id not in self.users or followee_id not in self.users:
            return False

        return self.graph.add_edge(follower_id, followee_id)

    def unfollow_user(self, follower_id: str, followee_id: str) -> bool:
        """Make one user unfollow another."""
        return self.graph.remove_edge(follower_id, followee_id)

    def get_following(self, user_id: str) -> List[Person]:
        """Get list of people a user is following."""
        following_ids = self.graph.list_outgoing_adjacent_vertices(user_id)
        return [self.users[uid] for uid in following_ids if uid in self.users]

    def get_followers(self, user_id: str) -> List[Person]:
        """Get list of people following a user."""
        follower_ids = self.graph.list_incoming_adjacent_vertices(user_id)
        return [self.users[uid] for uid in follower_ids if uid in self.users]

    def get_all_users(self) -> List[Person]:
        """Get all users in the app."""
        return list(self.users.values())

    def get_user(self, user_id: str) -> Optional[Person]:
        """Get a specific user by ID."""
        return self.users.get(user_id)


def create_sample_users() -> List[Person]:
    """Create sample user profiles."""
    users = [
        Person("alice123", "Alice Johnson", "Female",
               "Love traveling and photography! 📸✈️", Privacy.PUBLIC, 28, "New York"),
        Person("bob_dev", "Bob Smith", "Male",
               "Software developer | Coffee enthusiast ☕", Privacy.PUBLIC, 32, "San Francisco"),
        Person("charlie_art", "Charlie Brown", "Male",
               "Digital artist and designer 🎨", Privacy.PRIVATE, 25, "Los Angeles"),
        Person("diana_fit", "Diana Wilson", "Female",
               "Fitness trainer | Healthy living advocate 💪", Privacy.PUBLIC, 29, "Miami"),
        Person("eve_music", "Eve Martinez", "Female",
               "Musician and composer 🎵 | Classical pianist", Privacy.PRIVATE, 31, "Chicago"),
        Person("frank_chef", "Frank Thompson", "Male",
               "Professional chef | Food blogger 👨‍🍳", Privacy.PUBLIC, 35, "Austin"),
        Person("grace_writer", "Grace Lee", "Female",
               "Author and blogger | Love books and tea 📚☕", Privacy.PUBLIC, 27, "Seattle")
    ]
    return users


def setup_connections(app: SocialMediaApp):
    """Set up initial connections between users."""
    connections = [
        ("alice123", "bob_dev"),
        ("alice123", "diana_fit"),
        ("alice123", "frank_chef"),
        ("bob_dev", "alice123"),
        ("bob_dev", "charlie_art"),
        ("charlie_art", "eve_music"),
        ("charlie_art", "grace_writer"),
        ("diana_fit", "alice123"),
        ("diana_fit", "frank_chef"),
        ("eve_music", "grace_writer"),
        ("frank_chef", "alice123"),
        ("frank_chef", "diana_fit"),
        ("frank_chef", "grace_writer"),
        ("grace_writer", "eve_music"),
        ("grace_writer", "frank_chef")
    ]

    for follower, followee in connections:
        app.follow_user(follower, followee)


def display_user_profile(person: Person, respect_privacy: bool = False):
    """Display user profile information."""
    print(f"\n{'=' * 50}")
    print(f"USER PROFILE")
    print(f"{'=' * 50}")

    if respect_privacy and person.privacy == Privacy.PRIVATE:
        info = person.get_public_info()
        print(f"User ID: {info['user_id']}")
        print(f"Name: {info['name']}")
        print(f"Privacy: Private Profile")
        print("(Other details are hidden due to privacy settings)")
    else:
        info = person.get_full_info()
        print(f"User ID: {info['user_id']}")
        print(f"Name: {info['name']}")
        print(f"Gender: {info['gender'] or 'Not specified'}")
        print(f"Age: {info['age'] or 'Not specified'}")
        print(f"Location: {info['location'] or 'Not specified'}")
        print(f"Privacy: {info['privacy'].title()}")
        print(f"Biography: {info['biography'] or 'No biography available'}")


def display_user_selection_menu(app: SocialMediaApp) -> str:
    """Display user selection menu and return selected user ID."""
    users = app.get_all_users()
    print(f"\n{'=' * 50}")
    print("SELECT A USER:")
    print(f"{'=' * 50}")
    for i, user in enumerate(users, 1):
        print(f"{i}. {user.name} (@{user.user_id})")
    print(f"{'=' * 50}")

    while True:
        try:
            choice = input(f"Enter user number (1-{len(users)}) or user ID: ").strip()

            # Check if input is a number
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(users):
                    return users[index].user_id
                else:
                    print(f"❌ Please enter a number between 1 and {len(users)}")
            else:
                # Check if input is a valid user ID
                if app.get_user(choice):
                    return choice
                else:
                    print("❌ User ID not found! Please try again.")
        except ValueError:
            print("❌ Invalid input! Please enter a valid number or user ID.")


def main():
    """Main program with menu-driven interface."""
    # Initialize the app and create sample data
    app = SocialMediaApp()

    # Create and add sample users
    sample_users = create_sample_users()
    for user in sample_users:
        app.add_user(user)

    # Set up initial connections
    setup_connections(app)

    print("🌟 Welcome to Social Media Graph App! 🌟")
    print("Instagram-like social network simulation")

    while True:
        print(f"\n{'=' * 50}")
        print("           MAIN MENU")
        print(f"{'=' * 50}")
        print("1. Display list of all users")
        print("2. View profile of a person")
        print("3. View followed accounts of a person")
        print("4. View followers of a person")
        print("5. Exit")
        print(f"{'=' * 50}")

        # Advanced features menu (shown after mandatory features)
        print("\n🚀 ADVANCED FEATURES (Improvements):")
        print("6. Add new user profile")
        print("7. Follow a user")
        print("8. Unfollow a user")
        print(f"{'=' * 50}")

        try:
            choice = input("Enter your choice (1-8): ").strip()

            if choice == "5":
                print("Thank you for using Social Media Graph App! Goodbye! 👋")
                break

            elif choice == "1":
                # Display all users
                users = app.get_all_users()
                print(f"\n{'=' * 50}")
                print(f"ALL USERS ({len(users)} total)")
                print(f"{'=' * 50}")
                for i, user in enumerate(users, 1):
                    privacy_status = "🔒 Private" if user.privacy == Privacy.PRIVATE else "🌐 Public"
                    print(f"{i}. {user.name} (@{user.user_id}) - {privacy_status}")

            elif choice == "2":
                # View user profile with privacy consideration
                user_id = display_user_selection_menu(app)
                user = app.get_user(user_id)
                if user:
                    print(f"\n{'=' * 50}")
                    print(f"USER PROFILE")
                    print(f"{'=' * 50}")

                    # Always show name and user ID
                    print(f"Name: {user.name}")
                    print(f"User ID: @{user.user_id}")

                    # Show full details only for public accounts
                    if user.privacy == Privacy.PUBLIC:
                        print(f"Privacy: Public Profile 🌐")
                        print(f"Gender: {user.gender or 'Not specified'}")
                        print(f"Age: {user.age or 'Not specified'}")
                        print(f"Location: {user.location or 'Not specified'}")
                        print(f"Biography: {user.biography or 'No biography available'}")
                    else:
                        print(f"Privacy: Private Profile 🔒")
                        print("This account is private. Only the name is visible.")
                else:
                    print("❌ User not found!")

            elif choice == "3":
                # View following list (blocked for private accounts)
                user_id = display_user_selection_menu(app)
                user = app.get_user(user_id)
                if user:
                    # Check if account is private
                    if user.privacy == Privacy.PRIVATE:
                        print(f"\n{'=' * 50}")
                        print(f"{user.name}'s Following List")
                        print(f"{'=' * 50}")
                        print("🔒 This account is private.")
                        print("Following list is not visible for private accounts.")
                    else:
                        following = app.get_following(user_id)
                        print(f"\n{'=' * 50}")
                        print(f"{user.name} is following ({len(following)} people):")
                        print(f"{'=' * 50}")
                        if following:
                            for i, person in enumerate(following, 1):
                                privacy_status = "🔒" if person.privacy == Privacy.PRIVATE else "🌐"
                                print(f"{i}. {person.name} (@{person.user_id}) {privacy_status}")
                        else:
                            print("This user is not following anyone yet.")
                else:
                    print("❌ User not found!")

            elif choice == "4":
                # View followers list (blocked for private accounts)
                user_id = display_user_selection_menu(app)
                user = app.get_user(user_id)
                if user:
                    # Check if account is private
                    if user.privacy == Privacy.PRIVATE:
                        print(f"\n{'=' * 50}")
                        print(f"{user.name}'s Followers")
                        print(f"{'=' * 50}")
                        print("🔒 This account is private.")
                        print("Followers list is not visible for private accounts.")
                    else:
                        followers = app.get_followers(user_id)
                        print(f"\n{'=' * 50}")
                        print(f"{user.name}'s followers ({len(followers)} people):")
                        print(f"{'=' * 50}")
                        if followers:
                            for i, person in enumerate(followers, 1):
                                privacy_status = "🔒" if person.privacy == Privacy.PRIVATE else "🌐"
                                print(f"{i}. {person.name} (@{person.user_id}) {privacy_status}")
                        else:
                            print("This user has no followers yet.")
                else:
                    print("❌ User not found!")

            elif choice == "6":
                # Advanced Feature: Add new user
                print(f"\n{'=' * 40}")
                print("ADD NEW USER PROFILE")
                print(f"{'=' * 40}")
                user_id = input("Enter user ID: ").strip()
                if app.get_user(user_id):
                    print("❌ User ID already exists!")
                    continue

                name = input("Enter full name: ").strip()
                if not name:
                    print("❌ Name is required!")
                    continue

                gender = input("Enter gender (optional): ").strip()
                age_str = input("Enter age (optional): ").strip()
                age = int(age_str) if age_str.isdigit() else None
                location = input("Enter location (optional): ").strip()
                biography = input("Enter biography (optional): ").strip()

                privacy_choice = input("Privacy setting (1=Public, 2=Private): ").strip()
                privacy = Privacy.PRIVATE if privacy_choice == "2" else Privacy.PUBLIC

                new_user = Person(user_id, name, gender, biography, privacy, age, location)
                if app.add_user(new_user):
                    print(f"✅ User {name} (@{user_id}) added successfully!")
                else:
                    print("❌ Failed to add user!")

            elif choice == "7":
                # Advanced Feature: Follow a user
                print(f"\n{'=' * 40}")
                print("FOLLOW A USER")
                print(f"{'=' * 40}")
                print("Select the user who wants to follow someone:")
                follower_id = display_user_selection_menu(app)

                print("Select the user to follow:")
                followee_id = display_user_selection_menu(app)

                if follower_id == followee_id:
                    print("❌ A user cannot follow themselves!")
                    continue

                if app.follow_user(follower_id, followee_id):
                    follower = app.get_user(follower_id)
                    followee = app.get_user(followee_id)
                    print(f"✅ {follower.name} is now following {followee.name}!")
                else:
                    print("❌ Unable to follow user. They may already be following this person.")

            elif choice == "8":
                # Advanced Feature: Unfollow a user
                print(f"\n{'=' * 40}")
                print("UNFOLLOW A USER")
                print(f"{'=' * 40}")
                print("Select the user who wants to unfollow someone:")
                follower_id = display_user_selection_menu(app)

                # Show only users that the selected user is currently following
                following = app.get_following(follower_id)
                if not following:
                    print("❌ This user is not following anyone!")
                    continue

                print(f"\n{app.get_user(follower_id).name} is currently following:")
                for i, person in enumerate(following, 1):
                    print(f"{i}. {person.name} (@{person.user_id})")

                while True:
                    try:
                        choice_num = input(f"Enter number (1-{len(following)}) to unfollow: ").strip()
                        if choice_num.isdigit():
                            index = int(choice_num) - 1
                            if 0 <= index < len(following):
                                followee_id = following[index].user_id
                                break
                            else:
                                print(f"❌ Please enter a number between 1 and {len(following)}")
                        else:
                            print("❌ Please enter a valid number!")
                    except ValueError:
                        print("❌ Invalid input!")

                if app.unfollow_user(follower_id, followee_id):
                    follower = app.get_user(follower_id)
                    followee = app.get_user(followee_id)
                    print(f"✅ {follower.name} has unfollowed {followee.name}!")
                else:
                    print("❌ Unable to unfollow user.")

            else:
                print("❌ Invalid choice! Please enter a number between 1-8.")

        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye! 👋")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()