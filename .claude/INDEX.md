# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (279)

```
 10565  GET              /                                                dashboard
 16097  GET              /api/abo/status                                  api_abo_status
 10664  GET              /api/active-recordings                           api_active_recordings
 16172  GET              /api/activity-pulse                              api_activity_pulse
 15525  GET              /api/ai-log                                      api_ai_log
 11062  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 25250  GET              /api/ai/anomalies                                api_ai_anomalies
 12679  POST             /api/ai/ask                                      api_ai_ask
 13917  POST             /api/ai/claude/save                              api_claude_save
 13897  GET              /api/ai/claude/status                            api_claude_status
 13935  POST             /api/ai/claude/test                              api_claude_test
 12945  GET              /api/ai/config                                   api_ai_config
 11234  GET              /api/ai/conversations                            api_ai_conversations_list
 11245  POST             /api/ai/conversations                            api_ai_conversations_create
 11255  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get
 11278  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete
 11285  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch
 11296  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send
 11429  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream
 12020  POST             /api/ai/diagnose                                 api_ai_diagnose
 25488  GET              /api/ai/forecast-storage                         api_ai_forecast_storage
 25522  GET              /api/ai/health-score/<username>                  api_ai_health_score
 11218  GET              /api/ai/models                                   api_ai_models
 25203  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive
 25183  POST             /api/ai/query                                    api_ai_query
 25356  GET              /api/ai/recommendations                          api_ai_recommendations
 25404  GET              /api/ai/report                                   api_ai_report
 25455  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice
 25314  GET              /api/ai/segments                                 api_ai_segments
 25158  GET              /api/ai/skills                                   api_ai_skills
 15932  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 23576  GET/POST         /api/audio/config                                api_audio_config
 23606  POST             /api/audio/testtone                              api_audio_testtone
 16038  GET/POST         /api/auto-archive-rules                          api_archive_rules
 16062  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 16066  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12895  GET              /api/automation/status                           api_automation_status
 12917  POST             /api/automation/toggle                           api_automation_toggle
 14730  GET              /api/azrael/agents                               api_azrael_agents
 12798  POST             /api/azrael/ask                                  api_azrael_ask
 23812  GET/POST         /api/azrael/context                              api_azrael_context
 14357  GET              /api/azrael/core                                 api_azrael_core
 23946  POST             /api/azrael/live_pause                           api_azrael_live_pause
 23936  GET              /api/azrael/live_status                          api_azrael_live_status
 23954  POST             /api/azrael/live_test                            api_azrael_live_test
 14739  GET              /api/azrael/memories                             api_azrael_memories
 24002  POST             /api/azrael/persona                              api_azrael_persona_set
 23993  GET              /api/azrael/personas                             api_azrael_personas
 24030  GET              /api/azrael/piper_status                         api_azrael_piper_status
 23785  POST             /api/azrael/react                                api_azrael_react
 23821  GET              /api/azrael/reaction                             api_azrael_reaction
 23973  GET              /api/azrael/reactions                            api_azrael_reactions
 24023  GET              /api/azrael/transcript                           api_azrael_transcript
 23908  POST             /api/azrael/tts_test                             api_azrael_tts_test
 23883  GET              /api/azrael/voices                               api_azrael_voices
 24047  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11538  GET              /api/backoff-watch                               api_backoff_watch
 15296  POST             /api/backup/run                                  api_backup_run
 15262  GET              /api/backup/status                               api_backup_status
 15251  POST             /api/backup/system                               api_backup_system
 16004  GET              /api/bandwidth/live                              api_bandwidth_live
 15917  GET              /api/bookmarks                                   api_bookmarks_list
 11801  GET              /api/brain                                       api_brain
 11738  GET              /api/brain/alarms                                api_brain_alarms
 11723  GET              /api/brain/creator                               api_brain_creator
 11700  GET              /api/brain/graph                                 api_brain_graph
 11761  GET              /api/brain/growth                                api_brain_growth
 10161  GET              /api/brain/health                                api_brain_health
 24528  GET              /api/channel/categories                          api_channel_categories
 24534  POST             /api/channel/set                                 api_channel_set
 24344  GET              /api/channels/status                             api_channels_status
 23131  POST             /api/chat/send                                   api_chat_send
 14997  GET              /api/chat/send_status                            api_chat_send_status
 10645  GET              /api/checks                                      api_checks
 23849  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 23832  GET              /api/clips                                       api_clips
 23865  POST/DELETE      /api/clips/clear                                 api_clips_clear
 23451  GET              /api/cohost                                      api_cohost
 23463  POST             /api/cohost/config                               api_cohost_config
 16750  GET              /api/community/stats                             api_community_stats
 25860  POST             /api/config/restore                              api_config_restore
 25845  GET              /api/config/snapshot                             api_config_snapshot
 16195  GET              /api/cookies/age                                 api_cookies_age
 10712  GET              /api/cookies/health                              api_cookies_health
 10719  POST             /api/cookies/update                              api_cookies_update
 25811  GET              /api/data/export                                 api_data_export
 17260  GET              /api/db/export                                   api_db_export
 17287  POST             /api/db/import                                   api_db_import
 17247  GET              /api/db/summary                                  api_db_summary
 23377  GET              /api/debug/threads                               api_debug_threads
 26746  GET              /api/defense/attacks                             api_defense_attacks
 26713  GET              /api/defense/crowdsec                            api_defense_crowdsec
 26731  GET              /api/defense/fail2ban                            api_defense_fail2ban
 26437  GET              /api/defense/overview                            api_defense_overview
 15358  POST             /api/discord/announce                            api_discord_announce
 15086  GET              /api/discord/clips_week                          api_discord_clips_week
 15302  GET              /api/discord/community                           api_discord_community
 15025  GET              /api/discord/invite                              api_discord_invite
 14488  GET              /api/discord/overview                            api_discord_overview
 14574  POST             /api/discord/webhook_test                        api_discord_webhook_test
 16827  POST             /api/donations/add                               api_donations_add
 16860  GET              /api/donations/manual                            api_donations_manual
 16868  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 16763  POST             /api/donations/reset                             api_donations_reset
 16884  GET              /api/donations/summary                           api_donations_summary
 15986  GET              /api/events                                      api_events
 15133  GET              /api/events/stream                               api_events_stream
 17915  GET              /api/evolution/changelog                         api_evolution_changelog
 17900  GET              /api/evolution/history                           api_evolution_history
 17840  GET              /api/evolution/learned                           api_evolution_learned
 17862  GET              /api/evolution/proposals                         api_evolution_proposals
 17883  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 17830  POST             /api/evolution/run                               api_evolution_run
 17930  GET              /api/evolution/snapshots                         api_evolution_snapshots
 17795  GET              /api/evolution/status                            api_evolution_status
 17094  GET              /api/finanzamt/entries                           api_finanzamt_entries
 17114  POST             /api/finanzamt/entry                             api_finanzamt_add
 17141  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 15999  GET              /api/forecast/storage                            api_forecast_storage
 12933  GET              /api/freeai/status                               api_freeai_status
 14430  GET              /api/health                                      api_health
 16017  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 16013  GET              /api/heatmap/recordings                          api_heatmap_recordings
 23500  GET              /api/highlights                                  api_highlights
 23512  POST             /api/highlights/config                           api_highlights_config
 24385  GET              /api/kick/channel                                api_kick_channel
 24406  POST             /api/kick/channel                                api_kick_channel_set
 14157  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 14225  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 14203  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 14142  GET              /api/kick/oauth/start                            api_kick_oauth_start
 14182  GET              /api/kick/oauth/status                           api_kick_oauth_status
 23624  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 23693  POST             /api/kickmod/config                              api_kickmod_config
 23738  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 23752  GET              /api/kickmod/learned                             api_kickmod_learned
 23779  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 23759  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 24090  POST             /api/kickmod/say                                 api_kickmod_say
 24066  POST             /api/kickmod/start                               api_kickmod_start
 23664  GET              /api/kickmod/status                              api_kickmod_status
 24077  POST             /api/kickmod/stop                                api_kickmod_stop
 10497  POST             /api/login                                       dashboard_login_submit
 16735  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13384  POST             /api/marketing/config                            api_marketing_config
 13409  GET              /api/marketing/preview                           api_marketing_preview
 13419  POST             /api/marketing/send-now                          api_marketing_send_now
 13358  GET              /api/marketing/status                            api_marketing_status
 13376  POST             /api/marketing/toggle                            api_marketing_toggle
 23527  GET              /api/moderation/feed                             api_moderation_feed
 13988  POST             /api/news/config                                 api_news_config
 13954  GET              /api/news/creators                               api_news_creators
 13965  POST             /api/news/creators/generate                      api_news_creators_generate
 14030  POST             /api/news/generate-now                           api_news_generate_now
 14025  GET              /api/news/items                                  api_news_items
 14016  GET              /api/news/preview                                api_news_preview
 13884  GET              /api/news/status                                 api_news_status
 13980  POST             /api/news/toggle                                 api_news_toggle
 16592  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 14962  GET              /api/notify/status                               api_notify_status
 14973  POST             /api/notify/test                                 api_notify_test
 14948  GET              /api/ops/audit                                   api_ops_audit
 16663  GET              /api/ops/db-stats                                api_ops_db_stats
 16691  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14754  GET              /api/ops/errors                                  api_ops_errors
 16612  GET              /api/ops/healthcheck                             api_ops_healthcheck
 17342  GET              /api/ops/log-tail                                api_ops_log_tail
 12778  GET              /api/ops/logtail                                 api_ops_logtail
 14695  GET              /api/ops/metrics                                 api_ops_metrics
 14678  GET              /api/ops/resource_history                        api_ops_resource_history
 17316  GET              /api/ops/version                                 api_ops_version
 10915  GET              /api/outcomes                                    api_outcomes
 25009  POST             /api/overlay/config                              api_overlay_config
 24996  POST             /api/overlay/event                               api_overlay_event
 24901  GET              /api/overlay/state                               api_overlay_state
 10948  GET              /api/profile/<username>                          api_profile
 16203  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 16025  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 16151  GET              /api/proxy/heatmap                               api_proxy_heatmap
 16128  GET              /api/proxy/trend                                 api_proxy_trend
 13858  GET              /api/public/stats                                api_public_stats
 10599  GET              /api/pulse                                       api_pulse
 15549  GET              /api/recording-attempts                          api_recording_attempts
 23066  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 23044  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 23085  POST             /api/restream/<int:rid>/start                    api_restream_start
 23398  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 24863  GET              /api/restream/chatfeed                           api_restream_chatfeed
 23020  POST             /api/restream/create                             api_restream_create
 14233  GET              /api/restream/deck                               api_restream_deck
 12869  GET              /api/restream/health                             api_restream_health
 24885  POST             /api/restream/layout                             api_restream_layout
 22993  GET              /api/restream/list                               api_restream_list
 12842  POST             /api/restream/report                             api_restream_report
 23411  POST             /api/restream/start_all                          api_restream_start_all
 23437  POST             /api/restream/stop_all                           api_restream_stop_all
 13132  GET              /api/restream/testpush                           api_testpush_status
 13157  POST             /api/restream/testpush                           api_testpush_run
 17000  GET              /api/restream/verify                             api_restream_verify
 15064  GET              /api/retention/preview                           api_retention_preview
 15073  POST             /api/retention/run                               api_retention_run
 25926  POST             /api/schedule/add                                api_schedule_add
 25916  GET              /api/schedule/list                               api_schedule_list
 25951  POST             /api/schedule/remove                             api_schedule_remove
 15902  GET              /api/search                                      api_search
 26484  GET              /api/selftest                                    api_selftest
 23102  GET              /api/shield/stats                                api_shield_stats
 10618  GET              /api/stats                                       api_stats
 16166  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 16093  GET              /api/stats/tiktok-status                         api_tiktok_status
 25891  GET              /api/stats/timeline                              api_stats_timeline
 10686  GET              /api/storage                                     api_storage
 10693  POST             /api/storage/cleanup                             api_storage_cleanup
 16079  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12819  GET              /api/stream/timeline                             api_stream_timeline
 14562  GET              /api/stream/transcript                           api_stream_transcript
 25559  GET              /api/streamer/compare                            api_streamer_compare
 25758  POST             /api/streamer/delete/<username>                  api_streamer_delete
 15038  GET              /api/streamer/detail                             api_streamer_detail
 25783  GET              /api/streamer/digest/<username>                  api_streamer_digest
 25663  GET              /api/streamer/dormant                            api_streamer_dormant
 25739  GET              /api/streamer/exists/<username>                  api_streamer_exists
 25618  GET              /api/streamer/journal/<username>                 api_streamer_journal
 25583  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 25643  GET              /api/streamer/watchlist                          api_streamer_watchlist
 14397  GET              /api/streamers/wall                              api_streamers_wall
 10835  GET              /api/summary/preview                             api_summary_preview
 15614  GET              /api/system                                      api_system
 16948  GET              /api/system/check_timing                         api_check_timing
 17228  GET              /api/system/config_drift                         api_config_drift
 14598  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14809  GET              /api/system/preflight                            api_system_preflight
 14935  GET              /api/system/preflight_history                    api_system_preflight_history
 15198  GET              /api/system/resilience                           api_system_resilience
 15937  GET              /api/tags                                        api_tags_list
 10659  GET              /api/top                                         api_top
 12752  GET              /api/trackings                                   api_trackings
 16481  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 16514  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 15973  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 16186  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 16543  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 15959  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 15388  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 15435  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 15464  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 15446  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 10852  POST             /api/trackings/bulk                              api_trackings_bulk
 15403  GET              /api/trackings/export                            api_trackings_export
 15941  GET              /api/trackings/tags-map                          api_trackings_tags_map
 16241  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11593  GET              /api/trend-7d                                    api_trend_7d
 23897  GET              /api/tts/<fn>                                    api_tts_file
 13012  POST             /api/tunnel/set                                  api_tunnel_set
 12991  GET              /api/tunnel/status                               api_tunnel_status
 13023  POST             /api/tunnel/test                                 api_tunnel_test
 13004  POST             /api/tunnel/toggle                               api_tunnel_toggle
 17200  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 17177  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 17159  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 25037  GET              /api/upload_window                               api_upload_window
 10929  GET              /api/userstats                                   api_userstats
 14041  GET              /api/version                                     api_version
 17056  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 17077  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 17041  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 17025  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 30164  GET              /api/youtube/sendrate                            api_youtube_sendrate
 15587  GET              /archive/<int:eid>/download                      archive_download
 15644  GET              /download/<int:recording_id>                     download
 15510  GET              /health                                          health
 23346  GET              /healthz                                         healthz
 10486  GET              /login                                           dashboard_login_page
 10520  GET              /logout                                          dashboard_logout
 10527  GET              /manifest.webmanifest                            pwa_manifest
 14626  GET              /metrics                                         api_prometheus_metrics
 24846  GET              /overlay                                         overlay_page
 10551  GET              /pwa-icon-<variant>.png                          pwa_icon
 10537  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (66)

```
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   814  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   896  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   924  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   935  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   801  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   863  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   850  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   831  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   476  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   471  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   519  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   402  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   729  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   493  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   456  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   429  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   703  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   573  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   662  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   568  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   501  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   281  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   746  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   369  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   624  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   779  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   764  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   325  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   563  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   549  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   532  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   589  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   682  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   578  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 27189  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 27648  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 27280  /assign_role            Rolle/Gruppe einem Mitglied geben
 27326  /ban                    Mitglied bannen
 27980  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 27904  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 27944  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 27929  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 27771  /clips                  Letzte Highlight-Clips eines Users
 27241  /create_category        Kategorie anlegen
 27210  /create_channel         Text-Channel anlegen (optional in Kategorie)
 27269  /create_group           Nutzergruppe (= Rolle) anlegen
 27252  /create_role            Rolle / Nutzergruppe anlegen
 27226  /create_voice           Voice-Channel anlegen
 27562  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 27678  /event                  Community-Event ankündigen (Admin) — mit Countdown
 27721  /events                 Kommende Community-Events anzeigen
 27817  /follow                 Bei Live-Gang eines Streamers gepingt werden
 27801  /help                   Alle Bot-Befehle anzeigen
 27315  /kick                   Mitglied kicken
 27544  /leaderboard            Top-10 der Community nach XP
 27757  /livenow                Welche getrackten User sind gerade live
 27787  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 27618  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 27350  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 27530  /rank                   Dein Level und Rang anzeigen
 27744  /recstatus              Aktuell laufende Aufnahmen
 27291  /remove_role            Rolle/Gruppe entfernen
 27203  /restream_status        Restream-Status
 27302  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 27495  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 27513  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 27843  /stats                  Statistik zu einem getrackten Streamer
 27115  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 28139  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 28036  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 28012  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 27337  /timeout                Mitglied stummschalten (Minuten)
 27915  /topstreamers           Rangliste der Streamer nach Aufnahmen
 27145  /track                  TikTok-User tracken
 27129  /tracklist              Getrackte TikTok-User dieses Servers
 27832  /unfollow               Live-Pings für einen Streamer abbestellen
 27178  /untrack                TikTok-User nicht mehr tracken
 27865  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 27889  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 28623  on_member_join
 28585  on_message
 28226  on_raw_reaction_add
 28658  on_ready
```

## Top-Level-Symbole in bot_v37.py (562 Funktionen, 2 Klassen)

```
  2373-2374   _abo_key
  2394-2412   _abo_probe_dump
 26026-26036  _active_recorder_sync
 20306-20313  _ad_allowlist
 21419-21425  _agent_for
 26038-26056  _ai_calls_total_sync
 12665-12675  _ai_dashboard_rate_check
 21428-21444  _ai_telemetry
 21926-21944  _alert
 28771-28821  _alert_monitor_loop
 29195-29257  _announce_loop
  3315-3324   _anthropic_key
  3344-3356   _anthropic_model
  3327-3338   _anthropic_model_raw
 10289-10292  _arg_int
  2365-2370   _as_dict
 18512-18517  _audio_cfg
 22080-22102  _audio_tap_cmd
 10422-10433  _auth_cookie
 10389-10418  _auth_guard
  1521-1526   _auto_on
 22969-22987  _auto_restream_loop
 30325-30340  _azrael_broadcast_reply
 30225-30247  _azrael_chat_reply
 30208-30222  _azrael_chat_should_reply
 13584-13602  _azrael_creator_take
 30253-30255  _azrael_gate_cfg
 21449-21463  _azrael_live_state
 24745-24759  _azrael_overlay_state
 21809-21863  _azrael_proactive_loop
 21268-21324  _azrael_reaction_to_chats
 30258-30265  _azrael_reply_all_chats
 30195-30205  _azrael_self_names
 30293-30322  _azrael_send_to
 21466-21487  _azrael_system
 28935-28938  _backup_active
 29016-29029  _backup_loop
 20194-20195  _badwords_path
 28736-28745  _brain_growth_loop
 11669-11696  _brain_growth_snapshot
  2301-2321   _brain_hint_delay
 11661-11663  _brain_history_for
  6860-6888   _brain_notify
 11638-11659  _brain_record
 11665-11667  _brain_stream_recent
 15112-15129  _browser_push
 11189-11209  _build_context_for_llm
  6904-6991   _build_daily_summary
  2804-2984   _build_native_cmd
 18860-19047  _build_restream_cmd
  3028-3061   _build_ytdlp_cmd
 25978-25985  _cached_probe
  5682-5709   _can_stop_tracking
  1701-1723   _capture_set_cookies
 16289-16301  _cfg_get
 16304-16311  _cfg_set
 24489-24524  _channel_set_all
 18110-18113  _chat_connected
 18116-18132  _chat_disconnected
  8886-8897   _chat_is_forum
 18152-18154  _chat_sanitize
 18156-18165  _chat_src_ok
 18095-18107  _chat_stat
 18135-18138  _chat_stats_snapshot
  3698-3709   _check_ai_alive_sync
  3712-3724   _check_ai_models_sync
 25987-26000  _check_redis_alive_sync
 26002-26022  _check_redis_version_sync
 12360-12403  _classify_pool_anonymity
 12406-12423  _classify_pool_anonymity_bg
   754-758    _claude_chat_sync_metered
 10314-10321  _client_ip
 29289-29316  _clip_prune
 29319-29329  _clip_recfile_for
 29845-29851  _clip_should_velocity
 29370-29452  _clip_to_discord
  3517-3526   _close_ai_session
 30369-30384  _cohost_broadcast
 30351-30355  _cohost_cfg
 30410-30422  _cohost_fire_highlight
 30358-30366  _cohost_gate
 30387-30407  _cohost_highlight
 29501-29535  _community_events_loop
 11132-11168  _conv_add_message
 11171-11176  _conv_archive
 11107-11116  _conv_create
 11121-11129  _conv_messages
 11179-11186  _conv_rename
  7284-7324   _cookie_alarm_loop
  1773-1777   _cookie_autorefresh_info
  1678-1682   _cookie_header
 15162-15194  _cpu_load_snapshot
  3906-3918   _create_index_safe
 13552-13567  _creator_activity
 13608-13631  _creator_dossier_generate
 13570-13581  _creator_facts_line
 26239-26345  _crowdsec_status
 26205-26236  _crowdsec_via_lapi
 26070-26088  _cscli_bin
 26094-26107  _cscli_path
  7177-7202   _daily_summary_loop
 26125-26142  _darf_journal_lesen
 28748-28768  _db_maintenance_loop
  7149-7174   _db_vacuum_loop
 20329-20353  _detect_foreign_ad
  1278-1289   _diag_path_owner
 21715-21759  _director_finalize
 22526-22533  _director_for
 21664-21712  _director_mark
 29739-29774  _disc_automod_check
 29712-29718  _disc_state_get
 29721-29728  _disc_state_set
 26788-26801  _discord_guild_filesize_bytes
 26987-26996  _discord_invite
 29673-29709  _discord_live_thread
 21866-21878  _discord_notify
 26888-26913  _discord_ops_alert
 29571-29669  _discord_post_user
 27052-28733  _discord_run_once
 26926-26984  _discord_start
 29260-29266  _discord_stop
 26809-26811  _discord_upload_limit_label
 26804-26806  _discord_upload_limit_mb
  7205-7279   _disk_alarm_loop
 31638-31687  _disk_autoclean
 31690-31703  _disk_guard_loop
 31630-31635  _disk_pct
 24802-24805  _donations_unknown_count
 18469-18471  _drawtext_chain
 15741-15743  _dump_all_threads
 12285-12349  _enrich_proxies_with_geo
  1918-1962   _ensure_cookie_file_netscape
 26999-27049  _ensure_discord_invite
 29466-29498  _ensure_error_channel
 12528-12565  _ensure_proxy_ready
  8899-8922   _ensure_topic
   636-638    _env_int
   641-643    _env_int_range
 29538-29568  _error_channel_loop
 21910-21923  _event_webhook
 17403-17409  _evo_build_dir
 17412-17419  _evo_version
 17695-17776  _evolution_cycle
 17428-17448  _evolution_llm_note
 17779-17789  _evolution_loop
 17451-17692  _evolution_write_build
  6302-6336   _extract_file_payload
  2050-2052   _extract_urls_from_streamurl_node
 26110-26117  _f2b_sudo_hint
 21946-21948  _faster_whisper_available
 20218-20230  _fetch_ldnoobw_de
 12174-12192  _fetch_proxy_list
 22360-22388  _fetch_tiktok_room_id
   687-690    _ff_cmd
 16426-16439  _ffmpeg_version_str
 18632-18637  _find_chromium
  3021-3025   _find_external_recorder
  2055-2057   _find_stream_urls
 16354-16379  _fire_webhooks
  8060-8069   _fork_safe
   769-778    _freeai_chat_sync_metered
 26160-26202  _geo_lookup_ips
  3506-3515   _get_ai_session
  7894-7934   _get_live_info
  2591-2598   _get_resolve_semaphore
  8248-8613   _handle_single_tracking
 31482-31484  _hb
 31487-31504  _hb_while
 18170-18172  _highlight_cfg
 18175-18204  _highlight_observe
 18640-18645  _htmlov_screenshot_cmd
 22104-22114  _httpx_proxy
 16387-16399  _in_quiet_hours
 32471-32502  _install_fast_eventloop
 10184-10238  _install_fast_json
 15746-15762  _install_faulthandler
 23212-23221  _intel_ensure_schema
 23305-23336  _intel_index_loop
 23233-23243  _intel_index_one
 23224-23230  _intel_semantic
  5671-5680   _is_authorized
  8178-8184   _is_dead
  2040-2042   _is_hevc
 26145-26151  _is_private_ip
  1424-1431   _is_process_running
  6890-6901   _is_quiet_hours
  1086-1095   _is_upload_window
 10273-10286  _json_error_handler
  7107-7137   _kick_broadcaster_id
 13058-13077  _kick_channel_live
  7024-7066   _kick_follower_count
 14120-14133  _kick_oauth_exchange
 14136-14138  _kick_oauth_page
 14079-14083  _kick_redirect_public
 14070-14076  _kick_redirect_source
 14056-14067  _kick_redirect_uri
  7009-7011   _kick_slug
 14086-14117  _kick_user_token
  3955-3958   _kind_from_filename
 16416-16421  _latest_popularity
 20240-20246  _learned_load
 20237-20238  _learned_path
 20248-20256  _learned_save
 22741-22771  _live_react_loop
 22537-22730  _live_react_worker
 21327-21338  _live_transcript_push
 22732-22739  _live_users
 21762-21806  _living_title_loop
  3569-3579   _llm_list_models
 20197-20205  _load_banned_words_file
  1599-1672   _load_cookies_dict
 28941-29013  _local_backup_scan
 10255-10269  _log_5xx
 19055-19059  _looks_like_codec_err
 19050-19052  _looks_like_source_expired
  8141-8171   _loop_fehler
 15766-15775  _loop_heartbeat
 31452-31479  _loop_lag_monitor
 15885-15888  _loop_not_ready
 15778-15846  _loop_watchdog_thread
 21207-21221  _loyalty_add
 21198-21204  _loyalty_get
 21224-21232  _loyalty_top
 16800-16818  _manual_donations_rows
 16821-16823  _manual_donations_total
  8186-8187   _mark_dead
 13225-13254  _marketing_cfg
 13216-13222  _marketing_default_targets
 13211-13213  _marketing_enabled
 13268-13283  _marketing_flavor
 13338-13354  _marketing_loop
 13286-13296  _marketing_post_discord
 13299-13311  _marketing_post_telegram
 13314-13335  _marketing_publish
 13257-13261  _marketing_state_obj
 13264-13265  _marketing_state_save
 30272-30290  _maybe_handle_command
 31789-31813  _maybe_hype_clip
  3873-3896   _migrate_columns
 30547-30558  _mod_is_exempt
 30561-30566  _mod_warn_first
 30569-30572  _mod_warn_text
 17958-17966  _modlog
   890-892    _multistream_targets
  8072-8073   _nc_create_subprocess_exec
  8076-8077   _nc_create_subprocess_shell
 13449-13465  _news_cfg
 13436-13438  _news_enabled
 13503-13544  _news_facts
 13658-13680  _news_generate
 13863-13880  _news_loop
 13441-13446  _news_output_path
 13547-13549  _news_phrase
 13634-13655  _news_phrase_impl
 13478-13485  _news_read
 13468-13471  _news_state_obj
 13474-13475  _news_state_save
 13488-13500  _news_write
 25130-25154  _nl_to_sql
 17996-17998  _normalize_ingest
  2232-2249   _note_check_duration
 21353-21361  _oracle_memories
 21619-21653  _oracle_memorize
 21364-21377  _oracle_persona
 21346-21350  _oracle_recent_text
 18295-18303  _ov_atomic_write
 18283-18289  _ov_bar
 20153-20165  _ov_clip_text
 18292-18293  _ov_oneline
 24813-24842  _overlay_push
 18586-18629  _overlay_render_size
 18057-18061  _overlay_session_reset
 24761-24764  _overlay_src_ok
 20316-20326  _own_invites
 16781-16797  _parse_eur
 18581-18583  _parse_size
 26353-26433  _parse_ssh_attacks
  7496-7529   _pause_resume_cmd
  1727-1771   _persist_refreshed_cookies
  1565-1597   _pick_checked_pull_proxy
 10341-10346  _pin_auth_value
 10378-10379  _pin_clear_fail
 10358-10361  _pin_locked
 10364-10375  _pin_note_fail
 10349-10355  _pin_ok
 24651-24653  _piper_available
 24616-24638  _piper_list_voices
 24658-24683  _piper_pick_model
 24695-24742  _piper_say
 24609-24613  _piper_voice_roots
 16316-16351  _post_json_threaded
 18560-18578  _probe_video_size
  1452-1469   _proc_is_recorder
 12272-12283  _proxy_geo_cache_put
 12499-12525  _proxy_pool_refresh_loop
  1531-1562   _proxy_report_recording
 15731-15733  _prune_stall_dumps
 13683-13804  _public_stats
 21881-21907  _push_notify
 10480-10482  _pwa_dir
 12243-12258  _quick_validate_proxy
 16382-16384  _quiet_hours_config
 10445-10478  _rate_guard
 21172-21178  _react_warn
  7980-8019   _reap_proc
  2272-2294   _record_check_outcome
   682-684    _redact_stream_urls
 12426-12496  _refresh_proxy_pool
 24641-24647  _resolve_piper_model
  2066-2156   _resolve_via_html
  2414-2568   _resolve_via_webcast_api_v2
  2631-2693   _resolve_via_ytdlp
 29891-30020  _resolve_youtube_ingest
 22810-22817  _restream_active_platforms
 18042-18053  _restream_active_sources
 22391-22490  _restream_chat_guardian
 18207-18279  _restream_chat_push
 17969-17981  _restream_enabled
 18648-18735  _restream_html_overlay_start
 18738-18751  _restream_html_overlay_stop
  1034-1036   _restream_layout_mode
 18007-18030  _restream_overlay_files
 22775-22807  _restream_platform_state
 22931-22966  _restream_resume_after_restart
 18799-18857  _restream_tts_enqueue_wav
 18522-18554  _restream_tts_feeder
 18519-18520  _restream_tts_fifo_path
 18754-18781  _restream_tts_start
 18783-18797  _restream_tts_stop
 22820-22928  _restream_verify_loop
 28906-28918  _retention_loop
 28865-28903  _retention_scan
  2376-2378   _room_is_abo
  6340-6457   _run_ai_call
 15869-15882  _run_async_from_flask
 26154-26157  _run_priv
 32459-32467  _run_selfcheck_and_exit
 28921-28932  _s3_client
 25094-25125  _safe_select
  8189-8235   _safe_send
  4823-4839   _sample_net_throughput
 20207-20215  _save_banned_words_file
  2324-2351   _schedule_next_check
 28824-28862  _scheduler_loop
  3899-3903   _schema_pk
 15890-15895  _scraper_session
 30575-30614  _screen_full
 14446-14483  _sec_headers
  2045-2047   _select_stream_from_data_section
 32272-32456  _selfcheck
  1109-1113   _should_defer_upload
 29332-29367  _shrink_for_discord
 31710-31727  _sign_health_check
 31730-31749  _sign_health_loop
  8089-8100   _spawn
  8103-8133   _spawn_from_flask
 26477-26480  _st_befund
 22116-22357  _start_chat_listener
 15849-15866  _start_loop_watchdog
 13828-13854  _stats_loop
 13807-13810  _stats_output_path
 13813-13825  _stats_write
  8681-8695   _storage_cleanup_loop
 31769-31776  _story_for
  3083-3089   _stream_url_expiry
  3098-3104   _stream_url_is_fresh
  3091-3096   _stream_url_ttl
 20280-20287  _streamer_persona_get
 20262-20268  _streamer_personas_load
 20259-20260  _streamer_personas_path
 20270-20278  _streamer_personas_save
 18474-18478  _studio_chain
 29038-29160  _system_backup
 29163-29191  _system_backup_loop
 12195-12234  _test_proxy
 13099-13108  _testpush_cfg
 13111-13128  _testpush_exec
 13080-13096  _testpush_resolve_live
  8858-8868   _tg_topics_load_into_mem
  8855-8856   _tg_topics_path
  8870-8877   _tg_topics_save
 25687-25735  _tiktok_account_exists
 10324-10332  _token_ok
  8880-8884   _topic_forget
 16402-16413  _tracking_max_duration
  1336-1359   _try_attach_file_handler
 24685-24693  _tts_cleanup
 12984-12987  _tunnel_effective
 24111-24164  _twitch_channel_status
 30617-30759  _twitch_chat_loop
 30433-30534  _twitch_eventsub_loop
 17221-17224  _twitch_oauth_page
  1132-1145   _upload_queue_add
  1156-1158   _upload_queue_count
  1115-1124   _upload_queue_load
  1105-1107   _upload_queue_path
  1147-1154   _upload_queue_remove
  1126-1130   _upload_queue_save
  1160-1198   _upload_window_loop
  7953-7960   _uptime_s
 17984-17993  _url_host
   747-751    _usage_record_claude
  7069-7097   _viewer_sample_loop
  7139-7146   _viewer_stats
 10382-10385  _wants_html
  7963-7977   _warn_empty_env
 31525-31620  _watchdog_loop
 30174-30182  _wchat_thank_ok
 21950-21980  _whisper_get_model
  8050-8057   _whisper_native_section
 21159-21165  _whisper_pool
 22049-22078  _whisper_segments
 21982-22046  _whisper_transcribe
 18305-18467  _write_restream_overlay
 30787-30860  _youtube_api_chat_loop
 24167-24270  _youtube_api_status
 24273-24340  _youtube_channel_status
 30863-31020  _youtube_chat_loop
 30026-30039  _youtube_restream_autoconfig
 30042-30066  _youtube_restream_autoconfig_inner
 30132-30160  _youtube_send
 24445-24486  _youtube_set_channel
 30069-30103  _yt_access_token
 30106-30121  _yt_live_chat_id
 30780-30784  _yt_oauth_configured
 30127-30129  _yt_sendrate_cfg
 30762-30777  _yt_timeout
  2615-2616   _ytdlp_detect_available
  2618-2629   _ytdlp_note_result
 15736-15738  _zombie_child_count
  7830-7854   about
  4074-4093   add_ai_log_entry
  3991-3994   add_archive_entry
  4936-4951   add_archive_rule
  4518-4552   add_recording
  4179-4196   add_tracking
  4613-4630   add_tracking_tag
  6460-6493   ai
  3738-3777   ai_chat
  3811-3821   ai_history_append
  3823-3828   ai_history_clear
  3800-3809   ai_history_load
  3785-3798   ai_rate_limit_check
  6522-6530   aireset
 21490-21509  azrael_chat
 31025-31147  brain_cmd
  3107-3291   build_recording_cmd
  4199-4276   bulk_add_trackings
  7327-7386   bulkadd
  8698-8838   check_all_trackings
  4363-4375   claim_live_transition
 20356-21102  class KickModerator
 19062-20040  class RestreamManager
 12610-12652  classify_proxy_anonymity
  6568-6766   cleanup
  5531-5572   cleanup_old_recordings
  4509-4516   clear_recording
 29777-29842  clip_moment
  5084-5127   cluster_failures
  4767-4816   compute_storage_forecast
  7449-7493   cookies_cmd
  5373-5379   cookies_days_old
  4170-4176   count_trackings_for_chat
  4061-4072   decide_preferred_recorder
  4001-4004   delete_archive_entry
  4953-4961   delete_archive_rule
  5997-6144   diag
 31150-31211  einnahmen_cmd
  4761-4764   find_recordings_by_fingerprint
  4022-4038   finish_recording_attempt
  4308-4318   get_all_active_trackings
  4115-4118   get_all_checks
  4554-4557   get_all_recordings
  4655-4665   get_all_tags_with_counts
  4738-4741   get_annotations_for_recording
  3996-3999   get_archive_entry
  4731-4734   get_bookmarked_recordings
  1794-1911   get_cookie_health
  4604-4610   get_event_log
  4045-4059   get_last_recording_attempt
  2696-2801   get_live_status
  5287-5290   get_manual_recordings
  4746-4749   get_or_compute_inspect_sync
  5607-5651   get_outcome_breakdown
  4712-4720   get_priority_poll_interval
  4914-4923   get_profile_snapshots
  4095-4105   get_recent_ai_log
  4040-4043   get_recent_recording_attempts
  4559-4562   get_recording_by_id
  4724-4727   get_recording_note
  3454-3477   get_redis
  4146-4162   get_stats
  5498-5529   get_storage_stats
  4645-4653   get_tags_for_tracking
  5054-5068   get_tiktok_status_distribution
  4699-4710   get_tracking_priority
  4377-4386   get_tracking_state
  4304-4306   get_trackings_for_group
  5303-5306   get_trash_recordings
  9542-10152  handle_recording_finished
  3921-3946   init_db
  5421-5475   inspect_stream_url
 24808-24810  is_revenue_platform
  4926-4934   list_archive_rules
  5801-5839   live
  8238-8246   live_check_worker
  3529-3563   llm_chat
  3628-3695   llm_chat_stream_sync
  3597-3625   llm_chat_sync
  3582-3594   llm_list_models
  4570-4596   log_event
  1386-1419   log_recording_failure
  7643-7692   logs_cmd
 31817-32262  main
  6496-6519   on_ai_media
  7769-7795   on_ai_reply
  7798-7827   on_azrael_mention
  7859-7889   on_callback
 21512-21616  oracle_handle
  7532-7535   pause_tracking
  5661-5666   profile_keyboard
  5382-5418   quick_restart_tracking
  7594-7640   quota
  8615-8678   reaper_loop
  5050-5052   record_tiktok_status
  6535-6565   recstatus
  3479-3487   redis_get_json
  3489-3495   redis_set_json
  4278-4302   remove_tracking
  4632-4643   remove_tracking_tag
 31214-31224  report_cmd
 12655-12657  report_proxy_result
  2159-2186   resolve_tiktok_live_stream
  5298-5301   restore_recording
  7538-7541   resume_tracking
  4964-5044   run_archive_rules
 31227-31432  run_bot
 15658-15705  run_flask
  4842-4887   sample_bandwidth_for_active
  4893-4912   save_profile_snapshot
  4107-4113   save_tiktok_check
  4501-4507   set_recording_file
  4321-4359   set_tracking_paused
  4668-4697   set_tracking_priority
  5293-5296   soft_delete_recording
  8927-9540   split_and_send_video
  5714-5756   start
  4006-4020   start_recording_attempt
  6769-6807   stats
  5268-5285   stop_manual_recording
  7544-7591   stoprec
  6994-7002   summary_cmd
  7695-7766   sysres
  6146-6290   teststream
  5758-5799   tiktok
  7389-7446   topusers
  5876-5933   track
  5841-5873   track_exact
  5947-5995   tracklist
  5134-5266   trigger_manual_recording
  4462-4499   try_acquire_recording_lock
  5309-5368   universal_search
  5935-5945   untrack
  4756-4759   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              build_payload, chat_sync, is_retired, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           class MarketingConfig, class MarketingState, compose, has_content, next_due_ts, should_post, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                build_items, class NewsConfig, class NewsState, item_id, merge, render_json, should_generate
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       looks_like_source_expired, normalize_ingest
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
trackingdb.py          claim_transition, get_state
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
