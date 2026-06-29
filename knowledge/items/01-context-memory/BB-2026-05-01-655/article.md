# Beyond CLEAN and MVP: Architecting an Offline-first Reactive Data Layer in Android

- BestBlogs URL: https://www.bestblogs.dev/article/4f0d0408
- Original publisher URL: https://www.infoq.com/articles/rdla-offline-first-reactive-android-data-layer/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global
- Source: BestBlogs / InfoQ
- Publish time: 2026-06-24 17:00:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 5; page/content captured from BestBlogs resource APIs
- Extracted chars: 27455

---

Key Takeaways

    
     Reactive Data Layer Architecture (RDLA) eliminates the "boilerplate tax" of traditional Clean Architecture by enforcing a strict separation between public API data definition and private implementation sourcing.

     Developers can bypass the limitations of pull-based MVP patterns by utilizing cold Kotlin Flow streams to create a unidirectional, reactive data bus for the UI layer.

     For offline-first medical IoT, writing user modifications to a local Asynchronous Mutation Queue allows for immediate UI updates while backgrounding the actual network synchronization.

     Decoupling network call constraints from the UI via Android Jetpack WorkManager guarantees that critical data payloads succeed even if the user terminates the application.

     Implementing an internal TestExtensions interface allows engineers to run decoupled unit tests with Robolectric, validating database fallback logic without relying on fragile SQLite mocking.
      

       

    

   

   Preface

   Mobile applications operate in highly unpredictable environments. Users expect applications to load instantly, work offline, update in real-time, and save their data seamlessly despite intermittent cellular connectivity.

   While patterns like Model-View-Presenter (MVP) and CLEAN Architecture offer solid starting points for separation of concerns, they often fall short or introduce unnecessary boilerplate when applied to the unique, reactive demands of mobile platforms.

   This article introduces the Reactive Data Layer Architecture (RDLA)—a concrete, mobile-optimized pattern designed specifically to bridge the gap between reactive UI frameworks (like Jetpack Compose) and mobile storage constraints. By aligning these two boundaries, RDLA enables developers to build robust, offline-first, and reactive data layers.

   
   While RDLA is beneficial for any app requiring real-time UI updates and offline support, it becomes critical when interfacing with connected hardware or volatile data sources. For example, in the consumer medical IoT and wearable space—such as dual-node sleep wearables or self-fitting hearing aids—applications demand absolute reliability and synchronization.

   Unlike traditional REST API architectures built on stable network protocols, mobile data sourcing often deals with hardware APIs (like Bluetooth Low Energy) that rely on deeply nested, asynchronous callbacks executed across Binder threads. Without a reliable architecture to serialize operations and treat the local cache as the single source of truth, these systems quickly degenerate into state-synchronization bugs and flaky connections. For e..g BLE device based apps trigger the infamous "GATT race condition", causing the underlying Bluetooth controller to process commands out of order or drop them entirely (frequently resulting in poorly documented GATT Status 133 or 129 errors).

   RDLA addresses these challenges by treating the local cache as the definitive UI buffer while utilizing Kotlin Coroutines and suspendCancellableCoroutine bridges to serialize physical hardware operations. This transforms chaotic, multithreaded asynchronous events into deterministic, synchronous data streams.

   Drawing on architectural patterns developed for highly regulated consumer medical devices, we will use a Health Metric Tracking System (specifically tracking heart rate records) to explore the topology of RDLA, compare it to traditional patterns, and demonstrate its implementation in Kotlin.

   Limitations of Traditional Patterns

   Before diving into RDLA, let's analyze why traditional patterns can fall short in modern Android development.

   1. MVP: The Pull-Based Bottleneck

   In classic Model-View-Presenter (MVP), communication is procedural and pull-based:

   
    The Presenter asks the Model for data.

    The Model fetches the data and returns it via a callback.

    The Presenter pushes the data to the View.

   

   This works for simple applications, but it fails in reactive programming environments. If a background sync worker updates the database, the Presenter remains unaware of the change unless it polls the database or relies on a complex event bus. MVP lacks a native mechanism to propagate state changes downstream automatically.

   2. CLEAN Architecture: Mobile Misalignments

   CLEAN Architecture is excellent for keeping business logic independent of frameworks. However, when applied to mobile development without modification, it introduces two distinct challenges:

   
    The Boilerplate Tax (Pass-Through Use Cases): For simple read operations, classic CLEAN forces you to create a Use Case class that merely calls a Repository method. In database-heavy apps with dozens of tables, this results in a massive number of trivial, "pass-through" classes that add maintenance overhead without adding business value.

    Platform Agnosticism vs. Mobile Realities: CLEAN is designed to be database- and framework-agnostic. While this works well for enterprise backend systems, it does not address mobile-specific constraints. It offers no guidance on handling local-remote data synchronization, offline state propagation, or SQLite performance limits (such as database compilation boundaries).

   

   Introducing RDLA

   Reactive Data Layer Architecture (RDLA) is a pattern designed specifically to bridge the gap between reactive UI frameworks (like Jetpack Compose) and mobile storage constraints.

   RDLA enforces a strict separation between data definition (API) and data sourcing (Implementation), operating on three core principles:

   
    Reactive Push-Based Streams: The UI never queries data in a "one-shot" fashion. Instead, it subscribes to cold streams (Flow) of data.

    Local Cache as the Single Source of Truth: The UI reads data only from the local database. The network is used exclusively to populate this database.

    Encapsulated Caching & Sync: The logic of checking cache expiration, merging local edits, and triggering background fetches is hidden entirely inside the Repository implementation.

   

   The Architectural Topology

   RDLA splits your data package into three distinct modules: API, Implementation, and Database (Shared Storage).

   

   Figure 1: RDLA Architectural Topology and Module Boundaries 
      
 (Image Source: created by the author)

   [Click here to expand image above to full-size]

   RDLA in the Architectural Landscape: Fitting with Clean Architecture and MVVM

   RDLA is not a replacement for MVVM or Clean Architecture. Instead, it is a specialized, mobile-first implementation of the Data Layer (and parts of the Domain Layer) that integrates with them. It optimizes the interfaces between these patterns to eliminate common mobile-specific pain points.

   How RDLA Integrates with Clean Architecture

   Clean Architecture focuses on the Dependency Rule: code dependencies must only point inwards, toward the core business logic (Entities and Use Cases). RDLA strictly respects this rule but optimizes its implementation for mobile constraints:

   

   Figure 2: Mapping RDLA Modules to Clean Architecture Layers 
      
 (Image Source: created by the author)

   
    API Module (Entities): RDLA's API Module corresponds directly to Clean's innermost Entity layer. It contains only pure Kotlin data models (like HeartRateRecord) and the Repository interface. It has zero platform, database, or network dependencies.

    Repository Impl (Use Cases): In a classic Clean implementation, developers often write a Use Case class for every database read (e.g., GetHeartRateRecordsUseCase). RDLA eliminates this boilerplate for simple CRUD operations by allowing the presentation layer to observe the repository's reactive streams directly. However, for complex business logic that spans multiple domains (e.g., calculating heart rate variability based on sleep and cardio records), you still create a standard Clean Use Case class that depends on the RDLA Repository APIs.

    DataSource Interfaces (Interface Adapters): The private LocalDataSource and RemoteDataSource interfaces live in the Implementation Module, acting as the boundaries (Clean's Interface Adapters) that protect the repository from concrete database and network engines.

    Room DB & Retrofit Client (Frameworks & Drivers): The concrete implementations (RoomLocalDataSource, RetrofitRemoteDataSource) live in separate database and network modules. Framework details, such as Room annotations or serialization libraries, are entirely encapsulated at this outer boundary.

   

   How RDLA Drives MVVM (Unidirectional Data Flow)

   In traditional MVVM, the ViewModel often acts as an active manager that pulls data from a repository and manages its lifecycle. This imperatively managed data flow is prone to synchronization bugs.

   RDLA transforms this by converting the Model into a reactive data bus, enabling a strict Unidirectional Data Flow (UDF):

   

   Figure 3: Unidirectional Data Flow (UDF) Reactive Loop in RDLA 
      
 (Image Source: created by the author)

   
    ViewModel as a Transformer, Not a Synchronizer: Instead of launching coroutines to fetch data on demand and manually updating a state holder, the ViewModel in RDLA is a passive transformer. It observes the repository's Flow and converts it directly into a UI-consumable StateFlow using the stateIn operator.

    Automatic UI Synchronization: When a background sync worker or an offline mutation updates the Room database, the database automatically emits the new dataset. This change propagates through the repository and the ViewModel directly to the UI. The ViewModel does not need to poll or coordinate refreshing.

    Clear State Separation: RDLA allows the ViewModel to cleanly separate Persistent State (handled via StateFlow backed by Room) from Transient Events (handled via SharedFlow for one-time notifications like connection drops or errors).

   

   RDLA in Action: The Health Metric Tracking System

   To illustrate this architecture, we will build a data layer that tracks heart rate measurements.

   1. The API Module (Public)

   The API module is the only package visible to the UI layer. It contains pure domain models and repository interfaces.

   The Domain Model (HeartRateRecord.kt)

   This is a standard Kotlin data class with no database or serialization annotations.

   package com.example.healthtracker.data.heartrate.api.model

import java.time.Instant

data class HeartRateRecord(
    val id: String,
    val bpm: Int,
    val timestamp: Instant
)

   The Repository Interface (HeartRateRepository.kt)

   The interface defines the public contract. It exposes cold Flow streams.

   package com.example.healthtracker.data.heartrate.api

import com.example.healthtracker.data.heartrate.api.model.HeartRateRecord
import kotlinx.coroutines.flow.Flow
import java.time.Instant

interface HeartRateRepository {
    /**
     * Returns a reactive flow of heart rate records.
     * Triggers a network refresh in the background if the local cache is stale.
     */
    fun observeHeartRates(start: Instant, end: Instant): Flow<List<HeartRateRecord>>

    /**
     * Uploads new heart rate records. Suspends until the server confirms.
     */
    suspend fun upsertHeartRates(records: List<HeartRateRecord>)
}

   2. The Implementation Module (Private)

   Everything inside the implementation module is marked internal to prevent leaks. The UI layer can never access these classes directly.

   The Cache Wrapper (Cached.kt)

   To manage cache expiration without contaminating our domain model with metadata, we wrap our models in a Cached container inside the implementation layer:

   package com.example.healthtracker.data.core.caching

import java.time.Instant

data class Cached<out T>(
    val value: T,
    val insertionTime: Instant
)

   The Repository Coordinator (HeartRateFetchAndStoreRepository.kt)

   This class coordinates local and remote data sources. It checks cache expiration and triggers background fetches.

   package com.example.healthtracker.data.heartrate.impl

import com.example.healthtracker.data.heartrate.api.HeartRateRepository
import com.example.healthtracker.data.heartrate.api.model.HeartRateRecord
import com.example.healthtracker.data.heartrate.impl.local.HeartRateLocalDataSource
import com.example.healthtracker.data.heartrate.impl.remote.HeartRateRemoteDataSource
import com.example.healthtracker.data.core.caching.Cached
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flowOn
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onStart
import kotlinx.coroutines.launch
import java.time.Duration
import java.time.Instant
import kotlin.coroutines.CoroutineContext

internal class HeartRateFetchAndStoreRepository(
    private val localDS: HeartRateLocalDataSource,
    private val remoteDS: HeartRateRemoteDataSource,
    private val appScope: CoroutineScope,
    private val lightweightContext: CoroutineContext,
    private val cacheTtl: Duration = Duration.ofMinutes(10)
) : HeartRateRepository {

    override fun observeHeartRates(start: Instant, end: Instant): Flow<List<HeartRateRecord>> {
        return localDS.readHeartRates(start, end)
            .onStart { 
                // Asynchronous background refresh execution
                appScope.launch { triggerRefreshIfNeeded(start, end) } 
            }
            .map { cachedList -> cachedList.map { it.value } }
            .flowOn(lightweightContext)
    }

    private suspend fun triggerRefreshIfNeeded(start: Instant, end: Instant) {
        val cachedData = localDS.readHeartRatesOnce(start, end)
        if (cachedData.isEmpty() || isStale(cachedData)) {
            try {
                val remoteData = remoteDS.fetchHeartRates(start, end)
                localDS.writeHeartRates(remoteData)
            } catch (e: Exception) {
                // Fail silently; UI continues displaying cachedData
            }
        }
    }

    private fun isStale(data: List<Cached<HeartRateRecord>>): Boolean {
        val oldestAllowed = Instant.now().minus(cacheTtl)
        return data.any { it.insertionTime.isBefore(oldestAllowed) }
    }

    override suspend fun upsertHeartRates(records: List<HeartRateRecord>) {
        // Synchronous Mutation: Server write must succeed before updating DB
        val serverConfirmed = remoteDS.uploadHeartRates(records)
        localDS.writeHeartRates(serverConfirmed)
    }
}

   Note that by running triggerRefreshIfNeeded inside an application-scoped CoroutineScope (appScope), we ensure that database updates complete successfully even if the user exits the current screen, which has the effect of cancelling the ViewModel's scope.

   3. The Local Storage Module (Room)

   In a real-world mobile app, related features often share a database. RDLA introduces Transaction Groups to handle this. For example, heart rate and blood pressure data are grouped under the Cardio Transaction Group, sharing a single Room database instance.

   

   Figure 4: Room Local Storage Module Package Hierarchy under Cardio Transaction Group 
      
 (Image Source: created by the author)

   The Local Data Source Interface (HeartRateLocalDataSource.kt)

   interface HeartRateLocalDataSource {
    fun readHeartRates(start: Instant, end: Instant): Flow<List<Cached<HeartRateRecord>>>
    suspend fun readHeartRatesOnce(start: Instant, end: Instant): List<Cached<HeartRateRecord>>
    suspend fun writeHeartRates(records: List<HeartRateRecord>)
}

The Database Entity (HeartRateEntity.kt)
@Entity(tableName = "heart_rate_records")
data class HeartRateEntity(
    @PrimaryKey val id: String,
    val bpm: Int,
    val timestamp: Instant,
    val insertionTime: Instant
) {
    fun toModel() = HeartRateRecord(id = id, bpm = bpm, timestamp = timestamp)
}

   Room Implementation (HeartRateRoomDataSource.kt)

   internal class HeartRateRoomDataSource(
    private val dao: HeartRateDao,
    private val lightweightContext: CoroutineContext
) : HeartRateLocalDataSource {

    override fun readHeartRates(start: Instant, end: Instant): Flow<List<Cached<HeartRateRecord>>> {
        return dao.observeHeartRates(start, end)
            .distinctUntilChanged() // Prevents redundant emissions from Room
            .map { entities ->
                entities.map { Cached(it.toModel(), it.insertionTime) }
            }
            .flowOn(lightweightContext)
    }

    override suspend fun readHeartRatesOnce(start: Instant, end: Instant): List<Cached<HeartRateRecord>> {
        return dao.getHeartRates(start, end).map { Cached(it.toModel(), it.insertionTime) }
    }

    override suspend fun writeHeartRates(records: List<HeartRateRecord>) {
        val entities = records.map { 
            HeartRateEntity(it.id, it.bpm, it.timestamp, Instant.now()) 
        }
        dao.insertOrUpdate(entities)
    }
}

   TIP: We apply distinctUntilChanged() to Room flows. Because Room triggers table-level observation, any update to the table triggers an emission, even if the queried subset is unchanged. distinctUntilChanged() filters out these redundant events.

   4. The UI Layer (Compose) Consumption

   A reactive data layer is only as powerful as the presentation layer consuming it. To effectively bridge RDLA to Jetpack Compose, the UI layer aggregates the underlying data streams into a unified state representation using StateFlow. This ensures the UI accurately reflects the persistent state (such as Connected, Scanning, or Disconnected) regardless of the application lifecycle. Conversely, transient events—such as a localized sync rollback or a dropped BLE connection—bypass the permanent state. These are pushed to the UI via a highly configurable SharedFlow with a replay cache, ensuring that critical one-time alerts are preserved and delivered instantly even if the UI is temporarily destroyed during an orientation change.

   @HiltViewModel
class HeartRateViewModel @Inject constructor(
    private val repository: HeartRateRepository
) : ViewModel() {

    // Persistent state stream
    val uiState: StateFlow<UiState> = repository
        .observeHeartRates(Instant.now().minus(1, ChronoUnit.DAYS), Instant.now())
        .map { records -> UiState.Success(records) }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = UiState.Loading
        )

    // Transient event stream
    private val _faultEvents = MutableSharedFlow<FaultEvent>(
        replay = 1,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )
    val faultEvents = _faultEvents.asSharedFlow()
}

   By seamlessly integrating StateFlow for continuous states and SharedFlow for volatile hardware events, the ViewModel provides Compose with an impenetrable, reactive data bridge that guarantees the UI never displays stale or broken states.

   Designing for Offline Mutations

   Mutations are updates initiated by the user. Depending on the user experience requirements, mutations are processed either synchronously or asynchronously.

   1. Synchronous Mutations

   Synchronous mutations require the user to be online. If the network request fails, the local database remains unchanged, and the user is immediately prompted with an error (e.g., trying to delete medical logs).

   2. Asynchronous Mutations (Offline-First)

   For standard logs (like recording heart rate BPM during a workout), the write operation must succeed immediately, even offline. To achieve this, the mutation is written to a local database queue, merged on-the-fly into the active UI data flow, and synchronized in the background.

   

   Figure 5: Asynchronous Mutation Sync Pipeline and OS Background Delegation 
      
 (Image Source: created by the author)

   [Click here to expand image above to full-size]

   Implementing the Mutation Merger in the Local Data Source

   override fun readHeartRates(start: Instant, end: Instant): Flow<List<Cached<HeartRateRecord>>> {
    val savedRecordsFlow = dao.observeHeartRates(start, end)
    val pendingMutationsFlow = mutationDao.observePendingAddMutations()

    return savedRecordsFlow.combine(pendingMutationsFlow) { saved, mutations ->
        val mergedList = saved.map { Cached(it.toModel(), it.insertionTime) }.toMutableList()
        
        mutations.forEach { mutation ->
            if (mutation.timestamp in start..end) {
                // Overlay the local pending mutation on top of the list
                mergedList.removeAll { it.value.id == mutation.localId }
                mergedList.add(
                    Cached(
                        value = HeartRateRecord(mutation.localId, mutation.bpm, mutation.timestamp),
                        insertionTime = mutation.localCreationTime
                    )
                )
            }
        }
        mergedList.sortedByDescending { it.value.timestamp }
    }.flowOn(lightweightContext)
}

   RDLA distinctly splits background execution responsibilities between appScope Coroutines and Android Jetpack WorkManager. For immediate, synchronous data processing (such as saving an incoming health metric to the Room database), the architecture launches coroutines within an application-scoped CoroutineContext. This ensures that lightweight local database writes complete successfully even if the user swiftly navigates away, canceling the immediate ViewModel scope.

   However, for asynchronous mutations bridging the local database to the remote cloud (or pushing a multi-megabyte OTA firmware payload over BLE), appScope is insufficient. Android's aggressive power management features (Doze mode) and process-death mechanics can terminate the application mid-flight. For FDA-regulated health metrics, data drops are categorically unacceptable. By enqueuing asynchronous mutations via WorkManager, the sync request is delegated directly to the OS system service. This guarantees that critical payloads are executed with respect to strict systemic constraints (e.g., requiring unmetered Wi-Fi or sufficient battery) and will reliably resume exactly from the last known memory offset if a connection is severed.

   Background synchronization is managed via Android WorkManager, using a Hilt-injected CoroutineWorker. By decoupling the network call constraints from the UI, requests are guaranteed to succeed even if the user closes the app.

   Conflict Resolution and Rollbacks

   Optimistic local updates provide a seamless user experience, but they inherently invite collision. When the WorkManager sync worker attempts to upload the local mutation queue to the server, there is always a risk of remote rejection—for instance, an HTTP 409 Conflict if the record was modified concurrently by another authorized device, or a 422 Unprocessable Entity if the data fails clinical validation.

   In RDLA, the architecture must handle these rollbacks gracefully without corrupting the local single source of truth. When the remote API throws an HTTP exception, the worker catches the failure and flags the local mutation entity in Room as FAILED rather than initiating an infinite retry loop.

   The central repository, monitoring the health of the sync process, emits this failure state as a transient event to the UI layer via SharedFlow. Simultaneously, the local data source executes a database transaction to purge the rejected mutation from the queue. Because the UI layer is reactively collecting the merged flow, purging the pending mutation forces Room to trigger a new emission. The distinctUntilChanged() filter passes this updated state, and the UI instantly and automatically reverts to the last known, server-confirmed state.

   Why RDLA Makes Testing a Breeze

   One of the greatest benefits of RDLA is that it simplifies unit testing. By isolating Room database and Retrofit network configurations, you can test your repository logic directly.

   The TestExtensions Pattern

   Since your repository interface should not expose data insertion methods to the client (to prevent the UI from modifying the sync state directly), we introduce a testonly interface within the API target:

   

   Figure 6: The TestExtensions Seeding Pattern and Scope Boundary Separation 
      
 (Image Source: created by the author)

   1. Define the Test Extensions Interface (Lives in the API module)

   @VisibleForTesting
interface HeartRateRepositoryTestExtensions {
    suspend fun seedLocalHeartRates(records: List<HeartRateRecord>)
    suspend fun clearLocalCache()
}

   2. Implement the Interface in the Repository (Lives in the Impl module)

   internal class HeartRateFetchAndStoreRepository(
    private val localDS: HeartRateLocalDataSource,
    // ...
) : HeartRateRepository, HeartRateRepositoryTestExtensions {
    
    // Repository implementation...

    override suspend fun seedLocalHeartRates(records: List<HeartRateRecord>) {
        localDS.writeHeartRates(records)
    }

    override suspend fun clearLocalCache() {
        localDS.clearAll()
    }
}

   3. Write a Decoupled Unit Test (Using Robolectric)

   @HiltAndroidTest
@RunWith(AndroidJUnit4::class)
@Config(application = HiltTestApplication::class)
class HeartRateRepositoryTest {

    @get:Rule val hiltRule = HiltAndroidRule(this)

    @Inject lateinit var repository: HeartRateRepository
    @Inject lateinit var testExtensions: HeartRateRepositoryTestExtensions

    @Before
    fun setUp() {
        hiltRule.inject()
    }

    @Test
    fun observeHeartRates_emitsSeededData() = runTest {
        val now = Instant.now()
        val records = listOf(HeartRateRecord("1", 72, now))
        
        // Seed the database directly through the test extension
        testExtensions.seedLocalHeartRates(records)

        val flow = repository.observeHeartRates(now.minusSeconds(60), now.plusSeconds(60))
        
        assertThat(flow.first()).containsExactlyElementsIn(records)
    }
}

   Core Testing Benefits

   
    No SQLite Mocking: Using Robolectric with a real Room database ensures that your SQL queries are fully validated at test time.

    Robust Offlining Verification: By injecting a FakeHeartRateRemoteDataSource, you can configure network failures and assert that the repository Fallback logic handles the offline state gracefully.

    Decoupled Database Refactoring: If you refactor your SQLite schemas (e.g., adding database fields), your repository tests will not break, provided the mapping logic in the Local Data Source correctly translates database entities into domain models.

   

   Conclusion

   Building a responsive, offline-first Android application requires a data layer designed for reactivity. By applying the Reactive Data Layer Architecture (RDLA), you establish a clear boundary between public data API contracts and private, framework-specific data-source implementations. Consequently, your presentation layer (ViewModels/Presenters) operates in a purely reactive manner, observing data changes rather than procedurally querying them. Furthermore, RDLA simplifies testing by encouraging you to program to interfaces and utilize clean seeding patterns like TestExtensions.

   Ultimately, transitioning to RDLA provides your codebase with the structure needed to scale cleanly, handle synchronization challenges gracefully, and support the rich, offline-first experiences that modern users expect.
