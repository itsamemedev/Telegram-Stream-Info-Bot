# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (281)

```
 10594  GET              /                                                dashboard
 16307  GET              /api/abo/status                                  api_abo_status
 10693  GET              /api/active-recordings                           api_active_recordings
 16382  GET              /api/activity-pulse                              api_activity_pulse
 15632  GET              /api/ai-log                                      api_ai_log
 11091  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 25454  GET              /api/ai/anomalies                                api_ai_anomalies
 12786  POST             /api/ai/ask                                      api_ai_ask
 14024  POST             /api/ai/claude/save                              api_claude_save
 14004  GET              /api/ai/claude/status                            api_claude_status
 14042  POST             /api/ai/claude/test                              api_claude_test
 13052  GET              /api/ai/config                                   api_ai_config
 11263  GET              /api/ai/conversations                            api_ai_conversations_list
 11274  POST             /api/ai/conversations                            api_ai_conversations_create
 11284  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get
 11307  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete
 11314  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch
 11325  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send
 11458  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream
 12127  POST             /api/ai/diagnose                                 api_ai_diagnose
 25692  GET              /api/ai/forecast-storage                         api_ai_forecast_storage
 25726  GET              /api/ai/health-score/<username>                  api_ai_health_score
 11247  GET              /api/ai/models                                   api_ai_models
 25407  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive
 25387  POST             /api/ai/query                                    api_ai_query
 25560  GET              /api/ai/recommendations                          api_ai_recommendations
 25608  GET              /api/ai/report                                   api_ai_report
 25659  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice
 25518  GET              /api/ai/segments                                 api_ai_segments
 25362  GET              /api/ai/skills                                   api_ai_skills
 16142  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 23780  GET/POST         /api/audio/config                                api_audio_config
 23810  POST             /api/audio/testtone                              api_audio_testtone
 16248  GET/POST         /api/auto-archive-rules                          api_archive_rules
 16272  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 16276  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 13002  GET              /api/automation/status                           api_automation_status
 13024  POST             /api/automation/toggle                           api_automation_toggle
 14837  GET              /api/azrael/agents                               api_azrael_agents
 12905  POST             /api/azrael/ask                                  api_azrael_ask
 24016  GET/POST         /api/azrael/context                              api_azrael_context
 14464  GET              /api/azrael/core                                 api_azrael_core
 24150  POST             /api/azrael/live_pause                           api_azrael_live_pause
 24140  GET              /api/azrael/live_status                          api_azrael_live_status
 24158  POST             /api/azrael/live_test                            api_azrael_live_test
 14846  GET              /api/azrael/memories                             api_azrael_memories
 24206  POST             /api/azrael/persona                              api_azrael_persona_set
 24197  GET              /api/azrael/personas                             api_azrael_personas
 24234  GET              /api/azrael/piper_status                         api_azrael_piper_status
 23989  POST             /api/azrael/react                                api_azrael_react
 24025  GET              /api/azrael/reaction                             api_azrael_reaction
 24177  GET              /api/azrael/reactions                            api_azrael_reactions
 24227  GET              /api/azrael/transcript                           api_azrael_transcript
 24112  POST             /api/azrael/tts_test                             api_azrael_tts_test
 24087  GET              /api/azrael/voices                               api_azrael_voices
 24251  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11645  GET              /api/backoff-watch                               api_backoff_watch
 15403  POST             /api/backup/run                                  api_backup_run
 15369  GET              /api/backup/status                               api_backup_status
 15358  POST             /api/backup/system                               api_backup_system
 16214  GET              /api/bandwidth/live                              api_bandwidth_live
 16127  GET              /api/bookmarks                                   api_bookmarks_list
 11908  GET              /api/brain                                       api_brain
 11845  GET              /api/brain/alarms                                api_brain_alarms
 11830  GET              /api/brain/creator                               api_brain_creator
 11807  GET              /api/brain/graph                                 api_brain_graph
 11868  GET              /api/brain/growth                                api_brain_growth
 10190  GET              /api/brain/health                                api_brain_health
 24732  GET              /api/channel/categories                          api_channel_categories
 24738  POST             /api/channel/set                                 api_channel_set
 24548  GET              /api/channels/status                             api_channels_status
 23341  POST             /api/chat/send                                   api_chat_send
 15104  GET              /api/chat/send_status                            api_chat_send_status
 10674  GET              /api/checks                                      api_checks
 24053  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 24036  GET              /api/clips                                       api_clips
 24069  POST/DELETE      /api/clips/clear                                 api_clips_clear
 23655  GET              /api/cohost                                      api_cohost
 23667  POST             /api/cohost/config                               api_cohost_config
 16960  GET              /api/community/stats                             api_community_stats
 26064  POST             /api/config/restore                              api_config_restore
 26049  GET              /api/config/snapshot                             api_config_snapshot
 16405  GET              /api/cookies/age                                 api_cookies_age
 10741  GET              /api/cookies/health                              api_cookies_health
 10748  POST             /api/cookies/update                              api_cookies_update
 26015  GET              /api/data/export                                 api_data_export
 17470  GET              /api/db/export                                   api_db_export
 17497  POST             /api/db/import                                   api_db_import
 17457  GET              /api/db/summary                                  api_db_summary
 23581  GET              /api/debug/threads                               api_debug_threads
 26950  GET              /api/defense/attacks                             api_defense_attacks
 26917  GET              /api/defense/crowdsec                            api_defense_crowdsec
 26935  GET              /api/defense/fail2ban                            api_defense_fail2ban
 26641  GET              /api/defense/overview                            api_defense_overview
 15465  POST             /api/discord/announce                            api_discord_announce
 15193  GET              /api/discord/clips_week                          api_discord_clips_week
 15409  GET              /api/discord/community                           api_discord_community
 15132  GET              /api/discord/invite                              api_discord_invite
 14595  GET              /api/discord/overview                            api_discord_overview
 14681  POST             /api/discord/webhook_test                        api_discord_webhook_test
 17037  POST             /api/donations/add                               api_donations_add
 17070  GET              /api/donations/manual                            api_donations_manual
 17078  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 16973  POST             /api/donations/reset                             api_donations_reset
 17094  GET              /api/donations/summary                           api_donations_summary
 16196  GET              /api/events                                      api_events
 15240  GET              /api/events/stream                               api_events_stream
 18125  GET              /api/evolution/changelog                         api_evolution_changelog
 18110  GET              /api/evolution/history                           api_evolution_history
 18050  GET              /api/evolution/learned                           api_evolution_learned
 18072  GET              /api/evolution/proposals                         api_evolution_proposals
 18093  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 18040  POST             /api/evolution/run                               api_evolution_run
 18140  GET              /api/evolution/snapshots                         api_evolution_snapshots
 18005  GET              /api/evolution/status                            api_evolution_status
 17304  GET              /api/finanzamt/entries                           api_finanzamt_entries
 17324  POST             /api/finanzamt/entry                             api_finanzamt_add
 17351  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 16209  GET              /api/forecast/storage                            api_forecast_storage
 13040  GET              /api/freeai/status                               api_freeai_status
 14537  GET              /api/health                                      api_health
 11563  GET              /api/health-score                                api_health_score
 16227  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 16223  GET              /api/heatmap/recordings                          api_heatmap_recordings
 23704  GET              /api/highlights                                  api_highlights
 23716  POST             /api/highlights/config                           api_highlights_config
 24589  GET              /api/kick/channel                                api_kick_channel
 24610  POST             /api/kick/channel                                api_kick_channel_set
 14264  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 14332  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 14310  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 14249  GET              /api/kick/oauth/start                            api_kick_oauth_start
 14289  GET              /api/kick/oauth/status                           api_kick_oauth_status
 23828  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 23897  POST             /api/kickmod/config                              api_kickmod_config
 23942  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 23956  GET              /api/kickmod/learned                             api_kickmod_learned
 23983  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 23963  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 24294  POST             /api/kickmod/say                                 api_kickmod_say
 24270  POST             /api/kickmod/start                               api_kickmod_start
 23868  GET              /api/kickmod/status                              api_kickmod_status
 24281  POST             /api/kickmod/stop                                api_kickmod_stop
 10526  POST             /api/login                                       dashboard_login_submit
 16945  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13491  POST             /api/marketing/config                            api_marketing_config
 13516  GET              /api/marketing/preview                           api_marketing_preview
 13526  POST             /api/marketing/send-now                          api_marketing_send_now
 13465  GET              /api/marketing/status                            api_marketing_status
 13483  POST             /api/marketing/toggle                            api_marketing_toggle
 23731  GET              /api/moderation/feed                             api_moderation_feed
 14095  POST             /api/news/config                                 api_news_config
 14061  GET              /api/news/creators                               api_news_creators
 14072  POST             /api/news/creators/generate                      api_news_creators_generate
 14137  POST             /api/news/generate-now                           api_news_generate_now
 14132  GET              /api/news/items                                  api_news_items
 14123  GET              /api/news/preview                                api_news_preview
 13991  GET              /api/news/status                                 api_news_status
 14087  POST             /api/news/toggle                                 api_news_toggle
 16802  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 15069  GET              /api/notify/status                               api_notify_status
 15080  POST             /api/notify/test                                 api_notify_test
 15055  GET              /api/ops/audit                                   api_ops_audit
 16873  GET              /api/ops/db-stats                                api_ops_db_stats
 16901  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14861  GET              /api/ops/errors                                  api_ops_errors
 16822  GET              /api/ops/healthcheck                             api_ops_healthcheck
 17552  GET              /api/ops/log-tail                                api_ops_log_tail
 12885  GET              /api/ops/logtail                                 api_ops_logtail
 14802  GET              /api/ops/metrics                                 api_ops_metrics
 14785  GET              /api/ops/resource_history                        api_ops_resource_history
 17526  GET              /api/ops/version                                 api_ops_version
 10944  GET              /api/outcomes                                    api_outcomes
 25213  POST             /api/overlay/config                              api_overlay_config
 25200  POST             /api/overlay/event                               api_overlay_event
 25105  GET              /api/overlay/state                               api_overlay_state
 10977  GET              /api/profile/<username>                          api_profile
 16413  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 16235  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 16361  GET              /api/proxy/heatmap                               api_proxy_heatmap
 16338  GET              /api/proxy/trend                                 api_proxy_trend
 13965  GET              /api/public/stats                                api_public_stats
 10628  GET              /api/pulse                                       api_pulse
 15656  GET              /api/recording-attempts                          api_recording_attempts
 23276  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 23254  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 23295  POST             /api/restream/<int:rid>/start                    api_restream_start
 23602  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 25067  GET              /api/restream/chatfeed                           api_restream_chatfeed
 23230  POST             /api/restream/create                             api_restream_create
 14340  GET              /api/restream/deck                               api_restream_deck
 12976  GET              /api/restream/health                             api_restream_health
 25089  POST             /api/restream/layout                             api_restream_layout
 23203  GET              /api/restream/list                               api_restream_list
 12949  POST             /api/restream/report                             api_restream_report
 23615  POST             /api/restream/start_all                          api_restream_start_all
 23641  POST             /api/restream/stop_all                           api_restream_stop_all
 13239  GET              /api/restream/testpush                           api_testpush_status
 13264  POST             /api/restream/testpush                           api_testpush_run
 17210  GET              /api/restream/verify                             api_restream_verify
 15171  GET              /api/retention/preview                           api_retention_preview
 15180  POST             /api/retention/run                               api_retention_run
 26130  POST             /api/schedule/add                                api_schedule_add
 26120  GET              /api/schedule/list                               api_schedule_list
 26155  POST             /api/schedule/remove                             api_schedule_remove
 16112  GET              /api/search                                      api_search
 26688  GET              /api/selftest                                    api_selftest
 23312  GET              /api/shield/stats                                api_shield_stats
 10647  GET              /api/stats                                       api_stats
 16376  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 16303  GET              /api/stats/tiktok-status                         api_tiktok_status
 26095  GET              /api/stats/timeline                              api_stats_timeline
 10715  GET              /api/storage                                     api_storage
 10722  POST             /api/storage/cleanup                             api_storage_cleanup
 16289  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12926  GET              /api/stream/timeline                             api_stream_timeline
 14669  GET              /api/stream/transcript                           api_stream_transcript
 25763  GET              /api/streamer/compare                            api_streamer_compare
 25962  POST             /api/streamer/delete/<username>                  api_streamer_delete
 15145  GET              /api/streamer/detail                             api_streamer_detail
 25987  GET              /api/streamer/digest/<username>                  api_streamer_digest
 25867  GET              /api/streamer/dormant                            api_streamer_dormant
 25943  GET              /api/streamer/exists/<username>                  api_streamer_exists
 25822  GET              /api/streamer/journal/<username>                 api_streamer_journal
 25787  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 25847  GET              /api/streamer/watchlist                          api_streamer_watchlist
 14504  GET              /api/streamers/wall                              api_streamers_wall
 10864  GET              /api/summary/preview                             api_summary_preview
 15824  GET              /api/system                                      api_system
 15720  GET              /api/system-resources                            api_system_resources
 17158  GET              /api/system/check_timing                         api_check_timing
 17438  GET              /api/system/config_drift                         api_config_drift
 14705  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14916  GET              /api/system/preflight                            api_system_preflight
 15042  GET              /api/system/preflight_history                    api_system_preflight_history
 15305  GET              /api/system/resilience                           api_system_resilience
 16147  GET              /api/tags                                        api_tags_list
 10688  GET              /api/top                                         api_top
 12859  GET              /api/trackings                                   api_trackings
 16691  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 16724  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 16183  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 16396  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 16753  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 16169  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 15495  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 15542  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 15571  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 15553  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 10881  POST             /api/trackings/bulk                              api_trackings_bulk
 15510  GET              /api/trackings/export                            api_trackings_export
 16151  GET              /api/trackings/tags-map                          api_trackings_tags_map
 16451  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11700  GET              /api/trend-7d                                    api_trend_7d
 24101  GET              /api/tts/<fn>                                    api_tts_file
 13119  POST             /api/tunnel/set                                  api_tunnel_set
 13098  GET              /api/tunnel/status                               api_tunnel_status
 13130  POST             /api/tunnel/test                                 api_tunnel_test
 13111  POST             /api/tunnel/toggle                               api_tunnel_toggle
 17410  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 17387  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 17369  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 25241  GET              /api/upload_window                               api_upload_window
 10958  GET              /api/userstats                                   api_userstats
 14148  GET              /api/version                                     api_version
 17266  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 17287  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 17251  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 17235  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 30368  GET              /api/youtube/sendrate                            api_youtube_sendrate
 15694  GET              /archive/<int:eid>/download                      archive_download
 15854  GET              /download/<int:recording_id>                     download
 15617  GET              /health                                          health
 23550  GET              /healthz                                         healthz
 10515  GET              /login                                           dashboard_login_page
 10549  GET              /logout                                          dashboard_logout
 10556  GET              /manifest.webmanifest                            pwa_manifest
 14733  GET              /metrics                                         api_prometheus_metrics
 25050  GET              /overlay                                         overlay_page
 10580  GET              /pwa-icon-<variant>.png                          pwa_icon
 10566  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (64)

```
   356  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   620  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   502  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   485  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   477  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   313  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   329  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   664  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   629  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   649  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   536  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
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
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 27393  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 27852  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 27484  /assign_role            Rolle/Gruppe einem Mitglied geben
 27530  /ban                    Mitglied bannen
 28184  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 28108  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 28148  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 28133  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 27975  /clips                  Letzte Highlight-Clips eines Users
 27445  /create_category        Kategorie anlegen
 27414  /create_channel         Text-Channel anlegen (optional in Kategorie)
 27473  /create_group           Nutzergruppe (= Rolle) anlegen
 27456  /create_role            Rolle / Nutzergruppe anlegen
 27430  /create_voice           Voice-Channel anlegen
 27766  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 27882  /event                  Community-Event ankündigen (Admin) — mit Countdown
 27925  /events                 Kommende Community-Events anzeigen
 28021  /follow                 Bei Live-Gang eines Streamers gepingt werden
 28005  /help                   Alle Bot-Befehle anzeigen
 27519  /kick                   Mitglied kicken
 27748  /leaderboard            Top-10 der Community nach XP
 27961  /livenow                Welche getrackten User sind gerade live
 27991  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 27822  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 27554  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 27734  /rank                   Dein Level und Rang anzeigen
 27948  /recstatus              Aktuell laufende Aufnahmen
 27495  /remove_role            Rolle/Gruppe entfernen
 27407  /restream_status        Restream-Status
 27506  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 27699  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 27717  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 28047  /stats                  Statistik zu einem getrackten Streamer
 27319  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 28343  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 28240  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 28216  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 27541  /timeout                Mitglied stummschalten (Minuten)
 28119  /topstreamers           Rangliste der Streamer nach Aufnahmen
 27349  /track                  TikTok-User tracken
 27333  /tracklist              Getrackte TikTok-User dieses Servers
 28036  /unfollow               Live-Pings für einen Streamer abbestellen
 27382  /untrack                TikTok-User nicht mehr tracken
 28069  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 28093  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 28827  on_member_join
 28789  on_message
 28430  on_raw_reaction_add
 28862  on_ready
```

## Top-Level-Symbole in bot_v37.py (562 Funktionen, 2 Klassen)

```
  2368-2369   _abo_key
  2389-2407   _abo_probe_dump
 26230-26240  _active_recorder_sync
 20516-20523  _ad_allowlist
 21629-21635  _agent_for
 26242-26260  _ai_calls_total_sync
 12772-12782  _ai_dashboard_rate_check
 21638-21654  _ai_telemetry
 22136-22154  _alert
 28975-29025  _alert_monitor_loop
 29399-29461  _announce_loop
  3310-3319   _anthropic_key
  3339-3351   _anthropic_model
  3322-3333   _anthropic_model_raw
 10318-10321  _arg_int
  2360-2365   _as_dict
 18722-18727  _audio_cfg
 22290-22312  _audio_tap_cmd
 10451-10462  _auth_cookie
 10418-10447  _auth_guard
  1516-1521   _auto_on
 23179-23197  _auto_restream_loop
 30529-30544  _azrael_broadcast_reply
 30429-30451  _azrael_chat_reply
 30412-30426  _azrael_chat_should_reply
 13691-13709  _azrael_creator_take
 30457-30459  _azrael_gate_cfg
 21659-21673  _azrael_live_state
 24949-24963  _azrael_overlay_state
 22019-22073  _azrael_proactive_loop
 21478-21534  _azrael_reaction_to_chats
 30462-30469  _azrael_reply_all_chats
 30399-30409  _azrael_self_names
 30497-30526  _azrael_send_to
 21676-21697  _azrael_system
 29139-29142  _backup_active
 29220-29233  _backup_loop
 20404-20405  _badwords_path
 28940-28949  _brain_growth_loop
 11776-11803  _brain_growth_snapshot
  2296-2316   _brain_hint_delay
 11768-11770  _brain_history_for
  6889-6917   _brain_notify
 11745-11766  _brain_record
 11772-11774  _brain_stream_recent
 15219-15236  _browser_push
 11218-11238  _build_context_for_llm
  6933-7020   _build_daily_summary
  2799-2979   _build_native_cmd
 19070-19257  _build_restream_cmd
  3023-3056   _build_ytdlp_cmd
 26182-26189  _cached_probe
  5711-5738   _can_stop_tracking
  1696-1718   _capture_set_cookies
 16499-16511  _cfg_get
 16514-16521  _cfg_set
 24693-24728  _channel_set_all
 18320-18323  _chat_connected
 18326-18342  _chat_disconnected
  8915-8926   _chat_is_forum
 18362-18364  _chat_sanitize
 18366-18375  _chat_src_ok
 18305-18317  _chat_stat
 18345-18348  _chat_stats_snapshot
  3693-3704   _check_ai_alive_sync
  3707-3719   _check_ai_models_sync
 26191-26204  _check_redis_alive_sync
 26206-26226  _check_redis_version_sync
 12467-12510  _classify_pool_anonymity
 12513-12530  _classify_pool_anonymity_bg
   750-754    _claude_chat_sync_metered
 10343-10350  _client_ip
 29493-29520  _clip_prune
 29523-29533  _clip_recfile_for
 30049-30055  _clip_should_velocity
 29574-29656  _clip_to_discord
  3512-3521   _close_ai_session
 30573-30588  _cohost_broadcast
 30555-30559  _cohost_cfg
 30614-30626  _cohost_fire_highlight
 30562-30570  _cohost_gate
 30591-30611  _cohost_highlight
 29705-29739  _community_events_loop
 11161-11197  _conv_add_message
 11200-11205  _conv_archive
 11136-11145  _conv_create
 11150-11158  _conv_messages
 11208-11215  _conv_rename
  7313-7353   _cookie_alarm_loop
  1768-1772   _cookie_autorefresh_info
  1673-1677   _cookie_header
 15269-15301  _cpu_load_snapshot
  3901-3913   _create_index_safe
 13659-13674  _creator_activity
 13715-13738  _creator_dossier_generate
 13677-13688  _creator_facts_line
 26443-26549  _crowdsec_status
 26409-26440  _crowdsec_via_lapi
 26274-26292  _cscli_bin
 26298-26311  _cscli_path
  7206-7231   _daily_summary_loop
 26329-26346  _darf_journal_lesen
 28952-28972  _db_maintenance_loop
  7178-7203   _db_vacuum_loop
 20539-20563  _detect_foreign_ad
  1273-1284   _diag_path_owner
 21925-21969  _director_finalize
 22736-22743  _director_for
 21874-21922  _director_mark
 29943-29978  _disc_automod_check
 29916-29922  _disc_state_get
 29925-29932  _disc_state_set
 26992-27005  _discord_guild_filesize_bytes
 27191-27200  _discord_invite
 29877-29913  _discord_live_thread
 22076-22088  _discord_notify
 27092-27117  _discord_ops_alert
 29775-29873  _discord_post_user
 27256-28937  _discord_run_once
 27130-27188  _discord_start
 29464-29470  _discord_stop
 27013-27015  _discord_upload_limit_label
 27008-27010  _discord_upload_limit_mb
  7234-7308   _disk_alarm_loop
 31842-31891  _disk_autoclean
 31894-31907  _disk_guard_loop
 31834-31839  _disk_pct
 25006-25009  _donations_unknown_count
 18679-18681  _drawtext_chain
 15951-15953  _dump_all_threads
 12392-12456  _enrich_proxies_with_geo
  1913-1957   _ensure_cookie_file_netscape
 27203-27253  _ensure_discord_invite
 29670-29702  _ensure_error_channel
 12635-12672  _ensure_proxy_ready
  8928-8951   _ensure_topic
   631-633    _env_int
   636-638    _env_int_range
 29742-29772  _error_channel_loop
 22120-22133  _event_webhook
 17613-17619  _evo_build_dir
 17622-17629  _evo_version
 17905-17986  _evolution_cycle
 17638-17658  _evolution_llm_note
 17989-17999  _evolution_loop
 17661-17902  _evolution_write_build
  6331-6365   _extract_file_payload
  2045-2047   _extract_urls_from_streamurl_node
 26314-26321  _f2b_sudo_hint
 22156-22158  _faster_whisper_available
 20428-20440  _fetch_ldnoobw_de
 12281-12299  _fetch_proxy_list
 22570-22598  _fetch_tiktok_room_id
   682-685    _ff_cmd
 16636-16649  _ffmpeg_version_str
 18842-18847  _find_chromium
  3016-3020   _find_external_recorder
  2050-2052   _find_stream_urls
 16564-16589  _fire_webhooks
  8089-8098   _fork_safe
   765-774    _freeai_chat_sync_metered
 26364-26406  _geo_lookup_ips
  3501-3510   _get_ai_session
  7923-7963   _get_live_info
  2586-2593   _get_resolve_semaphore
  8277-8642   _handle_single_tracking
 31686-31688  _hb
 31691-31708  _hb_while
 18380-18382  _highlight_cfg
 18385-18414  _highlight_observe
 18850-18855  _htmlov_screenshot_cmd
 22314-22324  _httpx_proxy
 16597-16609  _in_quiet_hours
 32675-32706  _install_fast_eventloop
 10213-10267  _install_fast_json
 15956-15972  _install_faulthandler
 23422-23431  _intel_ensure_schema
 23509-23540  _intel_index_loop
 23443-23453  _intel_index_one
 23434-23440  _intel_semantic
  5700-5709   _is_authorized
  8207-8213   _is_dead
  2035-2037   _is_hevc
 26349-26355  _is_private_ip
  1419-1426   _is_process_running
  6919-6930   _is_quiet_hours
  1081-1090   _is_upload_window
 10302-10315  _json_error_handler
  7136-7166   _kick_broadcaster_id
 13165-13184  _kick_channel_live
  7053-7095   _kick_follower_count
 14227-14240  _kick_oauth_exchange
 14243-14245  _kick_oauth_page
 14186-14190  _kick_redirect_public
 14177-14183  _kick_redirect_source
 14163-14174  _kick_redirect_uri
  7038-7040   _kick_slug
 14193-14224  _kick_user_token
  3950-3958   _kind_from_filename
 16626-16631  _latest_popularity
 20450-20456  _learned_load
 20447-20448  _learned_path
 20458-20466  _learned_save
 22951-22981  _live_react_loop
 22747-22940  _live_react_worker
 21537-21548  _live_transcript_push
 22942-22949  _live_users
 21972-22016  _living_title_loop
  3564-3574   _llm_list_models
 20407-20415  _load_banned_words_file
  1594-1667   _load_cookies_dict
 29145-29217  _local_backup_scan
 10284-10298  _log_5xx
 19265-19269  _looks_like_codec_err
 19260-19262  _looks_like_source_expired
  8170-8200   _loop_fehler
 15976-15985  _loop_heartbeat
 31656-31683  _loop_lag_monitor
 16095-16098  _loop_not_ready
 15988-16056  _loop_watchdog_thread
 21417-21431  _loyalty_add
 21408-21414  _loyalty_get
 21434-21442  _loyalty_top
 17010-17028  _manual_donations_rows
 17031-17033  _manual_donations_total
  8215-8216   _mark_dead
 13332-13361  _marketing_cfg
 13323-13329  _marketing_default_targets
 13318-13320  _marketing_enabled
 13375-13390  _marketing_flavor
 13445-13461  _marketing_loop
 13393-13403  _marketing_post_discord
 13406-13418  _marketing_post_telegram
 13421-13442  _marketing_publish
 13364-13368  _marketing_state_obj
 13371-13372  _marketing_state_save
 30476-30494  _maybe_handle_command
 31993-32017  _maybe_hype_clip
  3868-3891   _migrate_columns
 30751-30762  _mod_is_exempt
 30765-30770  _mod_warn_first
 30773-30776  _mod_warn_text
 18168-18176  _modlog
   885-887    _multistream_targets
  8101-8102   _nc_create_subprocess_exec
  8105-8106   _nc_create_subprocess_shell
 13556-13572  _news_cfg
 13543-13545  _news_enabled
 13610-13651  _news_facts
 13765-13787  _news_generate
 13970-13987  _news_loop
 13548-13553  _news_output_path
 13654-13656  _news_phrase
 13741-13762  _news_phrase_impl
 13585-13592  _news_read
 13575-13578  _news_state_obj
 13581-13582  _news_state_save
 13595-13607  _news_write
 25334-25358  _nl_to_sql
 18206-18208  _normalize_ingest
  2227-2244   _note_check_duration
 21563-21571  _oracle_memories
 21829-21863  _oracle_memorize
 21574-21587  _oracle_persona
 21556-21560  _oracle_recent_text
 18505-18513  _ov_atomic_write
 18493-18499  _ov_bar
 20363-20375  _ov_clip_text
 18502-18503  _ov_oneline
 25017-25046  _overlay_push
 18796-18839  _overlay_render_size
 18267-18271  _overlay_session_reset
 24965-24968  _overlay_src_ok
 20526-20536  _own_invites
 16991-17007  _parse_eur
 18791-18793  _parse_size
 26557-26637  _parse_ssh_attacks
  7525-7558   _pause_resume_cmd
  1722-1766   _persist_refreshed_cookies
  1560-1592   _pick_checked_pull_proxy
 10370-10375  _pin_auth_value
 10407-10408  _pin_clear_fail
 10387-10390  _pin_locked
 10393-10404  _pin_note_fail
 10378-10384  _pin_ok
 24855-24857  _piper_available
 24820-24842  _piper_list_voices
 24862-24887  _piper_pick_model
 24899-24946  _piper_say
 24813-24817  _piper_voice_roots
 16526-16561  _post_json_threaded
 18770-18788  _probe_video_size
  1447-1464   _proc_is_recorder
 12379-12390  _proxy_geo_cache_put
 12606-12632  _proxy_pool_refresh_loop
  1526-1557   _proxy_report_recording
 15941-15943  _prune_stall_dumps
 13790-13911  _public_stats
 22091-22117  _push_notify
 10509-10511  _pwa_dir
 12350-12365  _quick_validate_proxy
 16592-16594  _quiet_hours_config
 10474-10507  _rate_guard
 21382-21388  _react_warn
  8009-8048   _reap_proc
  2267-2289   _record_check_outcome
   677-679    _redact_stream_urls
 12533-12603  _refresh_proxy_pool
 24845-24851  _resolve_piper_model
  2061-2151   _resolve_via_html
  2409-2563   _resolve_via_webcast_api_v2
  2626-2688   _resolve_via_ytdlp
 30095-30224  _resolve_youtube_ingest
 23020-23027  _restream_active_platforms
 18252-18263  _restream_active_sources
 22601-22700  _restream_chat_guardian
 18417-18489  _restream_chat_push
 18179-18191  _restream_enabled
 18858-18945  _restream_html_overlay_start
 18948-18961  _restream_html_overlay_stop
  1029-1031   _restream_layout_mode
 18217-18240  _restream_overlay_files
 22985-23017  _restream_platform_state
 23141-23176  _restream_resume_after_restart
 19009-19067  _restream_tts_enqueue_wav
 18732-18764  _restream_tts_feeder
 18729-18730  _restream_tts_fifo_path
 18964-18991  _restream_tts_start
 18993-19007  _restream_tts_stop
 23030-23138  _restream_verify_loop
 29110-29122  _retention_loop
 29069-29107  _retention_scan
  2371-2373   _room_is_abo
  6369-6486   _run_ai_call
 16079-16092  _run_async_from_flask
 26358-26361  _run_priv
 32663-32671  _run_selfcheck_and_exit
 29125-29136  _s3_client
 25298-25329  _safe_select
  8218-8264   _safe_send
  4852-4868   _sample_net_throughput
 20417-20425  _save_banned_words_file
  2319-2346   _schedule_next_check
 29028-29066  _scheduler_loop
  3894-3898   _schema_pk
 16100-16105  _scraper_session
 30779-30818  _screen_full
 14553-14590  _sec_headers
  2040-2042   _select_stream_from_data_section
 32476-32660  _selfcheck
  1104-1108   _should_defer_upload
 29536-29571  _shrink_for_discord
 31914-31931  _sign_health_check
 31934-31953  _sign_health_loop
  8118-8129   _spawn
  8132-8162   _spawn_from_flask
 26681-26684  _st_befund
 22326-22567  _start_chat_listener
 16059-16076  _start_loop_watchdog
 13935-13961  _stats_loop
 13914-13917  _stats_output_path
 13920-13932  _stats_write
  8710-8724   _storage_cleanup_loop
 31973-31980  _story_for
  3078-3084   _stream_url_expiry
  3093-3099   _stream_url_is_fresh
  3086-3091   _stream_url_ttl
 20490-20497  _streamer_persona_get
 20472-20478  _streamer_personas_load
 20469-20470  _streamer_personas_path
 20480-20488  _streamer_personas_save
 18684-18688  _studio_chain
 29242-29364  _system_backup
 29367-29395  _system_backup_loop
 12302-12341  _test_proxy
 13206-13215  _testpush_cfg
 13218-13235  _testpush_exec
 13187-13203  _testpush_resolve_live
  8887-8897   _tg_topics_load_into_mem
  8884-8885   _tg_topics_path
  8899-8906   _tg_topics_save
 25891-25939  _tiktok_account_exists
 10353-10361  _token_ok
  8909-8913   _topic_forget
 16612-16623  _tracking_max_duration
  1331-1354   _try_attach_file_handler
 24889-24897  _tts_cleanup
 13091-13094  _tunnel_effective
 24315-24368  _twitch_channel_status
 30821-30963  _twitch_chat_loop
 30637-30738  _twitch_eventsub_loop
 17431-17434  _twitch_oauth_page
  1127-1140   _upload_queue_add
  1151-1153   _upload_queue_count
  1110-1119   _upload_queue_load
  1100-1102   _upload_queue_path
  1142-1149   _upload_queue_remove
  1121-1125   _upload_queue_save
  1155-1193   _upload_window_loop
  7982-7989   _uptime_s
 18194-18203  _url_host
   743-747    _usage_record_claude
  7098-7126   _viewer_sample_loop
  7168-7175   _viewer_stats
 10411-10414  _wants_html
  7992-8006   _warn_empty_env
 31729-31824  _watchdog_loop
 30378-30386  _wchat_thank_ok
 22160-22190  _whisper_get_model
  8079-8086   _whisper_native_section
 21369-21375  _whisper_pool
 22259-22288  _whisper_segments
 22192-22256  _whisper_transcribe
 18515-18677  _write_restream_overlay
 30991-31064  _youtube_api_chat_loop
 24371-24474  _youtube_api_status
 24477-24544  _youtube_channel_status
 31067-31224  _youtube_chat_loop
 30230-30243  _youtube_restream_autoconfig
 30246-30270  _youtube_restream_autoconfig_inner
 30336-30364  _youtube_send
 24649-24690  _youtube_set_channel
 30273-30307  _yt_access_token
 30310-30325  _yt_live_chat_id
 30984-30988  _yt_oauth_configured
 30331-30333  _yt_sendrate_cfg
 30966-30981  _yt_timeout
  2610-2611   _ytdlp_detect_available
  2613-2624   _ytdlp_note_result
 15946-15948  _zombie_child_count
  7859-7883   about
  4103-4122   add_ai_log_entry
  3991-3999   add_archive_entry
  4965-4980   add_archive_rule
  4547-4581   add_recording
  4208-4225   add_tracking
  4642-4659   add_tracking_tag
  6489-6522   ai
  3733-3772   ai_chat
  3806-3816   ai_history_append
  3818-3823   ai_history_clear
  3795-3804   ai_history_load
  3780-3793   ai_rate_limit_check
  6551-6559   aireset
 21700-21719  azrael_chat
 31229-31351  brain_cmd
  3102-3286   build_recording_cmd
  4228-4305   bulk_add_trackings
  7356-7415   bulkadd
  8727-8867   check_all_trackings
  4392-4404   claim_live_transition
 20566-21312  class KickModerator
 19272-20250  class RestreamManager
 12717-12759  classify_proxy_anonymity
  6597-6795   cleanup
  5560-5601   cleanup_old_recordings
  4538-4545   clear_recording
 29981-30046  clip_moment
  5113-5156   cluster_failures
  4796-4845   compute_storage_forecast
  7478-7522   cookies_cmd
  5402-5408   cookies_days_old
  4199-4205   count_trackings_for_chat
  4090-4101   decide_preferred_recorder
  4009-4033   delete_archive_entry
  4982-4990   delete_archive_rule
  6026-6173   diag
 31354-31415  einnahmen_cmd
  4790-4793   find_recordings_by_fingerprint
  4051-4067   finish_recording_attempt
  4337-4347   get_all_active_trackings
  4144-4147   get_all_checks
  4583-4586   get_all_recordings
  4684-4694   get_all_tags_with_counts
  4767-4770   get_annotations_for_recording
  4001-4007   get_archive_entry
  4760-4763   get_bookmarked_recordings
  1789-1906   get_cookie_health
  4633-4639   get_event_log
  4074-4088   get_last_recording_attempt
  2691-2796   get_live_status
  5316-5319   get_manual_recordings
  4775-4778   get_or_compute_inspect_sync
  5636-5680   get_outcome_breakdown
  4741-4749   get_priority_poll_interval
  4943-4952   get_profile_snapshots
  4124-4134   get_recent_ai_log
  4069-4072   get_recent_recording_attempts
  4588-4591   get_recording_by_id
  4753-4756   get_recording_note
  3449-3472   get_redis
  4175-4191   get_stats
  5527-5558   get_storage_stats
  4674-4682   get_tags_for_tracking
  5083-5097   get_tiktok_status_distribution
  4728-4739   get_tracking_priority
  4406-4415   get_tracking_state
  4333-4335   get_trackings_for_group
  5332-5335   get_trash_recordings
  9571-10181  handle_recording_finished
  3916-3941   init_db
  5450-5504   inspect_stream_url
 25012-25014  is_revenue_platform
  4955-4963   list_archive_rules
  5830-5868   live
  8267-8275   live_check_worker
  3524-3558   llm_chat
  3623-3690   llm_chat_stream_sync
  3592-3620   llm_chat_sync
  3577-3589   llm_list_models
  4599-4625   log_event
  1381-1414   log_recording_failure
  7672-7721   logs_cmd
 32021-32466  main
  6525-6548   on_ai_media
  7798-7824   on_ai_reply
  7827-7856   on_azrael_mention
  7888-7918   on_callback
 21722-21826  oracle_handle
  7561-7564   pause_tracking
  5690-5695   profile_keyboard
  5411-5447   quick_restart_tracking
  7623-7669   quota
  8644-8707   reaper_loop
  5079-5081   record_tiktok_status
  6564-6594   recstatus
  3474-3482   redis_get_json
  3484-3490   redis_set_json
  4307-4331   remove_tracking
  4661-4672   remove_tracking_tag
 31418-31428  report_cmd
 12762-12764  report_proxy_result
  2154-2181   resolve_tiktok_live_stream
  5327-5330   restore_recording
  7567-7570   resume_tracking
  4993-5073   run_archive_rules
 31431-31636  run_bot
 15868-15915  run_flask
  4871-4916   sample_bandwidth_for_active
  4922-4941   save_profile_snapshot
  4136-4142   save_tiktok_check
  4530-4536   set_recording_file
  4350-4388   set_tracking_paused
  4697-4726   set_tracking_priority
  5322-5325   soft_delete_recording
  8956-9569   split_and_send_video
  5743-5785   start
  4035-4049   start_recording_attempt
  6798-6836   stats
  5297-5314   stop_manual_recording
  7573-7620   stoprec
  7023-7031   summary_cmd
  7724-7795   sysres
  6175-6319   teststream
  5787-5828   tiktok
  7418-7475   topusers
  5905-5962   track
  5870-5902   track_exact
  5976-6024   tracklist
  5163-5295   trigger_manual_recording
  4491-4528   try_acquire_recording_lock
  5338-5397   universal_search
  5964-5974   untrack
  4785-4788   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
archive.py             compute_recording_fingerprint, evaluate_archive_rule, get_archive_entries_paged, run_archive_file_check
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
